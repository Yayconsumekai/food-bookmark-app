from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.recommendation_service import (
    get_personalised,
    get_by_category,
    get_available_categories,
    get_random,
)
from app.services.ml_suggestion_service import get_ml_suggestions

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.get("/landing")
def landing_page(
    category: str     = Query(None),
    db:       Session = Depends(get_db),
    user:     User    = Depends(get_current_user),
):
    """
    Returns all 3 lists for the landing page in one request.
    Optionally filter list 2 by a specific category.
    """
    categories  = get_available_categories(db)
    chosen_cat  = category or (categories[0] if categories else "Desserts")

    return {
        "for_you":    get_personalised(db, user.id, limit=10),
        "by_category": {
            "category": chosen_cat,
            "recipes":  get_by_category(db, chosen_cat, limit=10),
        },
        "discover":   get_random(db, limit=10),
        "categories": categories,    # full list for the picker dropdown
    }


@router.get("/categories")
def list_categories(
    db:   Session = Depends(get_db),
    _:    User    = Depends(get_current_user),
):
    return get_available_categories(db)


@router.get("/folder/{folder_id}")
def folder_suggestions(
    folder_id: int,
    limit:     int     = Query(12, ge=1, le=30),
    db:        Session = Depends(get_db),
    user:      User    = Depends(get_current_user),
):
    """
    ML-based suggestions for a specific folder.
    Uses TF-IDF + cosine similarity (not kNN).
    """
    suggestions = get_ml_suggestions(db, user.id, folder_id, limit=limit)
    return {
        "folder_id":   folder_id,
        "method":      "TF-IDF Cosine Similarity",
        "suggestions": suggestions,
    }