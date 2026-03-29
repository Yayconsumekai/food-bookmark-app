from sqlalchemy.orm import Session
from sqlalchemy import text, func
from app.models.bookmark import Bookmark
from app.models.recipe   import Recipe
from typing import List
import random

# ── List 1: Personalised "For You" ───────────────────────────────────────────

def get_personalised(db: Session, user_id: int, limit: int = 10) -> List[dict]:
    """
    Find recipes similar to what the user has bookmarked.
    Strategy:
      1. Collect categories and keywords from all bookmarked recipes
      2. Build a tsquery from those terms
      3. Exclude already-bookmarked recipes
      4. Rank by ts_rank_cd + original recipe rating
    """
    # Fetch user's bookmarked recipe ids and their text fields
    bookmarked = (
        db.query(Bookmark.recipe_id, Recipe.category, Recipe.keywords)
        .join(Recipe, Recipe.id == Bookmark.recipe_id)
        .filter(Bookmark.user_id == user_id)
        .all()
    )

    if not bookmarked:
        # Cold start — return top rated recipes
        return get_top_rated(db, limit=limit)

    bookmarked_ids = [row.recipe_id for row in bookmarked]

    # Build a vocabulary from the user's bookmarks
    terms = set()
    for row in bookmarked:
        if row.category:
            terms.update(row.category.lower().split())
        if row.keywords:
            terms.update(row.keywords.lower().split()[:8])  # top 8 keywords

    # Remove very common stop words
    stopwords = {'and', 'or', 'the', 'with', 'a', 'an', 'of', 'in', 'for'}
    terms -= stopwords

    if not terms:
        return get_top_rated(db, limit=limit)

    import re
    clean_terms = [re.sub(r'[^a-zA-Z0-9]', '', t) for t in terms if re.match(r'^[a-zA-Z]', t)]
    clean_terms = [t for t in clean_terms if len(t) >= 2]
    if not clean_terms:
        return get_top_rated(db, limit=limit)
    tsquery = " | ".join(clean_terms[:15])

    sql = text("""
        SELECT
            id, name, image_url, category,
            rating, total_time, calories,
            ts_rank_cd(search_vector, query) AS rank
        FROM
            recipes,
            to_tsquery('english', :tsquery) query
        WHERE
            search_vector @@ query
            AND id != ALL(:excluded)
            AND rating IS NOT NULL
            AND image_url IS NOT NULL
        ORDER BY
            (ts_rank_cd(search_vector, query) * 0.4 + COALESCE(rating, 0) * 0.12) DESC
        LIMIT :limit
    """)

    rows = db.execute(sql, {
        "tsquery":  tsquery,
        "excluded": bookmarked_ids,
        "limit":    limit,
    }).fetchall()

    return [dict(r._mapping) for r in rows]


# ── List 2: Browse by Category ────────────────────────────────────────────────

def get_by_category(db: Session, category: str, limit: int = 10) -> List[dict]:
    """Return top-rated recipes from a specific category."""
    rows = (
        db.query(Recipe)
        .filter(Recipe.category.ilike(f"%{category}%"))
        .filter(Recipe.image_url.isnot(None))
        .filter(Recipe.rating.isnot(None))
        .order_by(Recipe.rating.desc())
        .limit(limit)
        .all()
    )
    return [_recipe_to_dict(r) for r in rows]


def get_available_categories(db: Session, limit: int = 20) -> List[str]:
    """Return the most populated categories for the category picker."""
    rows = db.execute(text("""
        SELECT category, COUNT(*) as cnt
        FROM recipes
        WHERE category IS NOT NULL AND category != ''
        GROUP BY category
        ORDER BY cnt DESC
        LIMIT :limit
    """), {"limit": limit}).fetchall()
    return [row.category for row in rows]


# ── List 3: Random Discovery ──────────────────────────────────────────────────

def get_random(db: Session, limit: int = 10) -> List[dict]:
    """Return completely random recipes using PostgreSQL TABLESAMPLE."""
    rows = db.execute(text("""
        SELECT id, name, image_url, category, rating, total_time, calories
        FROM recipes TABLESAMPLE SYSTEM(1)   -- sample ~1% of table
        WHERE image_url IS NOT NULL
        ORDER BY RANDOM()
        LIMIT :limit
    """), {"limit": limit}).fetchall()

    # Fallback if TABLESAMPLE returns too few rows
    if len(rows) < limit:
        rows = db.execute(text("""
            SELECT id, name, image_url, category, rating, total_time, calories
            FROM recipes
            WHERE image_url IS NOT NULL
            ORDER BY RANDOM()
            LIMIT :limit
        """), {"limit": limit}).fetchall()

    return [dict(r._mapping) for r in rows]


# ── Top rated fallback ────────────────────────────────────────────────────────

def get_top_rated(db: Session, limit: int = 10) -> List[dict]:
    rows = (
        db.query(Recipe)
        .filter(Recipe.rating.isnot(None))
        .order_by(Recipe.rating.desc())
        .limit(limit)
        .all()
    )
    return [_recipe_to_dict(r) for r in rows]


# ── Helper ────────────────────────────────────────────────────────────────────

def _recipe_to_dict(r: Recipe) -> dict:
    return {
        "id":         r.id,
        "name":       r.name,
        "image_url":  r.image_url,
        "category":   r.category,
        "rating":     r.rating,
        "total_time": r.total_time,
        "calories":   r.calories,
    }