from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.recipe import Recipe
from typing import Optional, List
import re

def build_tsquery(query: str) -> str:
    """
    Convert a plain search string into a PostgreSQL tsquery.
    e.g. 'chicken garlic soup' → 'chicken & garlic & soup'
    Strips special characters that would break tsquery syntax.
    """
    words = re.findall(r'[a-zA-Z0-9]+', query.lower())
    if not words:
        return None
    return " & ".join(words)

def search_recipes(
    db: Session,
    query: str,
    limit: int = 20,
    offset: int = 0,
) -> dict:
    """
    Full-text search using PostgreSQL tsvector + GIN index.
    Falls back to LIKE search for SQLite (used in testing).
    """
    tsquery = build_tsquery(query)
    if not tsquery:
        return {"results": [], "total": 0}

    dialect = db.get_bind().dialect.name

    if dialect == "postgresql":
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
            ORDER BY rank DESC
            LIMIT  :limit
            OFFSET :offset
        """)
        count_sql = text("""
            SELECT COUNT(*) FROM recipes,
                to_tsquery('english', :tsquery) query
            WHERE search_vector @@ query
            AND image_url IS NOT NULL
        """)
        rows  = db.execute(sql, {"tsquery": tsquery, "limit": limit, "offset": offset}).fetchall()
        total = db.execute(count_sql, {"tsquery": tsquery}).scalar()
        results = [dict(row._mapping) for row in rows]

    else:
        # SQLite fallback for testing — simple LIKE search
        words = re.findall(r'[a-zA-Z0-9]+', query.lower())
        q = db.query(Recipe)
        for word in words:
            q = q.filter(
                Recipe.name.ilike(f"%{word}%") |
                Recipe.ingredients.ilike(f"%{word}%") |
                Recipe.keywords.ilike(f"%{word}%")
            )
        total   = q.count()
        recipes = q.offset(offset).limit(limit).all()
        results = [
            {
                "id": r.id, "name": r.name, "image_url": r.image_url,
                "category": r.category, "rating": r.rating,
                "total_time": r.total_time, "calories": r.calories,
                "rank": 0.0,
            }
            for r in recipes
        ]

    return {"results": results, "total": total}