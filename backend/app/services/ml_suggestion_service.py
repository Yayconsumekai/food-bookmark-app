from sqlalchemy.orm import Session
from sqlalchemy import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.recipe   import Recipe
from app.models.bookmark import Bookmark
import numpy as np
import logging

logger = logging.getLogger(__name__)

# ── Module-level cache ────────────────────────────────────────────────────────
# TF-IDF matrix is expensive to build — we cache it across requests
_tfidf_matrix  = None
_tfidf_vectorizer = None
_recipe_ids    = []     # maps matrix row index → recipe id


def _build_tfidf_corpus(db: Session):
    """
    Build TF-IDF matrix over all recipes.
    Combines name (3x weight), category, keywords, and ingredients.
    Cached in memory after first call.
    """
    global _tfidf_matrix, _tfidf_vectorizer, _recipe_ids

    if _tfidf_matrix is not None:
        return   # already built

    logger.info("Building TF-IDF matrix — this runs once at startup...")

    rows = db.execute(text("""
        SELECT id, name, category, keywords, ingredients
        FROM recipes
        ORDER BY id
    """)).fetchall()

    corpus = []
    ids    = []

    for row in rows:
        # Weight name more heavily by repeating it 3 times
        name        = (row.name       or '') + ' '
        name_heavy  = (name * 3)
        category    = (row.category   or '')
        keywords    = (row.keywords   or '')
        ingredients = (row.ingredients or '')

        doc = f"{name_heavy} {category} {keywords} {ingredients}"
        corpus.append(doc.lower())
        ids.append(row.id)

    _tfidf_vectorizer = TfidfVectorizer(
        max_features=15000,   # vocabulary size cap
        ngram_range=(1, 2),   # unigrams + bigrams
        min_df=2,             # ignore very rare terms
        stop_words='english',
        sublinear_tf=True,    # apply log normalization to TF
    )

    _tfidf_matrix = _tfidf_vectorizer.fit_transform(corpus)
    _recipe_ids   = ids
    logger.info(f"TF-IDF matrix built: {_tfidf_matrix.shape}")


def get_ml_suggestions(
    db:        Session,
    user_id:   int,
    folder_id: int,
    limit:     int = 12,
) -> list:
    """
    Generate ML-based recipe suggestions for a folder using
    TF-IDF + Cosine Similarity (content-based filtering).

    Steps:
      1. Get all recipe_ids in the folder (seed set)
      2. Build / retrieve TF-IDF matrix
      3. Average the TF-IDF vectors of the seed recipes → "folder profile"
      4. Compute cosine similarity of profile vs all recipes
      5. Rank and return top matches not already in folder
    """
    _build_tfidf_corpus(db)

    # Get seed recipe ids (all bookmarks in this folder)
    bookmarks = (
        db.query(Bookmark.recipe_id)
        .filter(
            Bookmark.user_id  == user_id,
            Bookmark.folder_id == folder_id,
        )
        .all()
    )

    if not bookmarks:
        return []

    seed_ids   = {bm.recipe_id for bm in bookmarks}
    id_to_idx  = {rid: i for i, rid in enumerate(_recipe_ids)}

    # Get TF-IDF row indices for seed recipes
    seed_indices = [id_to_idx[rid] for rid in seed_ids if rid in id_to_idx]

    if not seed_indices:
        return []

    # Average seed vectors to create a "folder profile"
    seed_matrix     = _tfidf_matrix[seed_indices]
    folder_profile  = np.asarray(seed_matrix.mean(axis=0))   # shape: (1, vocab)

    # Cosine similarity: profile vs entire corpus
    similarities    = cosine_similarity(folder_profile, _tfidf_matrix)[0]

    # Sort by similarity descending, exclude seeds
    ranked_indices  = np.argsort(similarities)[::-1]

    results = []
    for idx in ranked_indices:
        rid   = _recipe_ids[idx]
        score = float(similarities[idx])

        if rid in seed_ids:
            continue   # already in folder
        if score < 0.05:
            break      # too dissimilar — stop early

        results.append((rid, score))
        if len(results) >= limit:
            break

    if not results:
        return []

    # Fetch full recipe data for matched ids
    result_ids    = [r[0] for r in results]
    score_map     = {r[0]: r[1] for r in results}

    recipes = (
        db.query(Recipe)
        .filter(Recipe.id.in_(result_ids))
        .all()
    )

    # Re-sort by similarity score (DB query may return in different order)
    recipes.sort(key=lambda r: score_map.get(r.id, 0), reverse=True)

    return [
        {
            "id":           r.id,
            "name":         r.name,
            "image_url":    r.image_url,
            "category":     r.category,
            "rating":       r.rating,
            "total_time":   r.total_time,
            "calories":     r.calories,
            "similarity":   round(score_map.get(r.id, 0), 4),
        }
        for r in recipes
    ]