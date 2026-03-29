from sqlalchemy.orm import Session
from sqlalchemy import text
from app.services.query_expansion_service import build_expanded_tsquery
from typing import Optional
import re


def build_tsquery(query: str) -> str:
    words = re.findall(r'[a-zA-Z0-9]+', query.lower())
    if not words:
        return None
    return " & ".join(words)


def search_recipes(
    db:          Session,
    query:       str,
    limit:       int   = 20,
    offset:      int   = 0,
    expand:      bool  = True,
    category:    str   = None,
    min_rating:  float = None,
    max_minutes: int   = None,
) -> dict:
    if expand:
        tsquery, expansion = build_expanded_tsquery(query)
    else:
        tsquery   = build_tsquery(query)
        expansion = {"has_expansions": False, "expansions_used": {}}

    if not tsquery:
        return {"results": [], "total": 0, "expansion": None, "facets": {}}

    facet_clauses = "AND image_url IS NOT NULL"
    params        = {"tsquery": tsquery, "limit": limit, "offset": offset}

    if category:
        facet_clauses      += " AND category ILIKE :category"
        params["category"]  = f"%{category}%"

    if min_rating is not None:
        facet_clauses        += " AND rating >= :min_rating"
        params["min_rating"]  = min_rating

    if max_minutes is not None:
        facet_clauses          += " AND total_minutes <= :max_minutes"
        params["max_minutes"]   = max_minutes

    sql = text(f"""
        SELECT
            id, name, image_url, category,
            rating, total_time, calories,
            ts_rank_cd(search_vector, query) AS rank
        FROM
            recipes,
            to_tsquery('english', :tsquery) query
        WHERE
            search_vector @@ query
            {facet_clauses}
        ORDER BY rank DESC
        LIMIT  :limit
        OFFSET :offset
    """)

    count_sql = text(f"""
        SELECT COUNT(*) FROM recipes,
            to_tsquery('english', :tsquery) query
        WHERE search_vector @@ query
        {facet_clauses}
    """)

    rows  = db.execute(sql,       params).fetchall()
    total = db.execute(count_sql, params).scalar()
    facets = _get_facets(db, tsquery)

    return {
        "results":   [dict(r._mapping) for r in rows],
        "total":     total,
        "expansion": expansion if expansion["has_expansions"] else None,
        "facets":    facets,
    }


def _get_facets(db: Session, tsquery: str) -> dict:
    category_sql = text("""
        SELECT category, COUNT(*) as count
        FROM recipes,
             to_tsquery('english', :tsquery) query
        WHERE search_vector @@ query
          AND image_url IS NOT NULL
          AND category IS NOT NULL
          AND category != ''
        GROUP BY category
        ORDER BY count DESC
        LIMIT 50                        
    """)

    rating_sql = text("""
        SELECT
            CASE
                WHEN rating >= 4.5 THEN '4.5+'
                WHEN rating >= 4.0 THEN '4.0+'
                WHEN rating >= 3.0 THEN '3.0+'
                ELSE 'Any'
            END as band,
            COUNT(*) as count
        FROM recipes,
             to_tsquery('english', :tsquery) query
        WHERE search_vector @@ query
          AND image_url IS NOT NULL
        GROUP BY band
        ORDER BY band DESC
    """)

    categories = db.execute(category_sql, {"tsquery": tsquery}).fetchall()
    ratings    = db.execute(rating_sql,   {"tsquery": tsquery}).fetchall()

    return {
        "categories": [{"name": r.category, "count": r.count} for r in categories],
        "ratings":    [{"band": r.band,     "count": r.count} for r in ratings],
    }