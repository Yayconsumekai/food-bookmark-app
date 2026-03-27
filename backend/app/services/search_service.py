from sqlalchemy.orm import Session
from sqlalchemy import text
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
    Returns ranked results and total count.
    """
    tsquery = build_tsquery(query)
    if not tsquery:
        return {"results": [], "total": 0}

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
    """)

    rows  = db.execute(sql,       {"tsquery": tsquery, "limit": limit, "offset": offset}).fetchall()
    total = db.execute(count_sql, {"tsquery": tsquery}).scalar()

    results = [dict(row._mapping) for row in rows]
    return {"results": results, "total": total}