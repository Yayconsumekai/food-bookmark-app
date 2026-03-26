from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.search_service import search_recipes
from app.services.spell_service import check_query
from app.schemas.recipe import RecipeCard, RecipeDetail
from app.models.recipe import Recipe

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("/")
def search(
    q:      str            = Query(..., min_length=1),
    limit:  int            = Query(20, ge=1, le=100),
    offset: int            = Query(0,  ge=0),
    db:     Session        = Depends(get_db),
    _:      User           = Depends(get_current_user),   # must be logged in
):
    results = search_recipes(db, q, limit=limit, offset=offset)
    return results


@router.get("/spell-check")
def spell_check(
    q:  str     = Query(..., min_length=1),
    db: Session = Depends(get_db),
    _:  User    = Depends(get_current_user),
):
    return check_query(q, db)


@router.get("/recipe/{recipe_id}", response_model=RecipeDetail)
def get_recipe(
    recipe_id: int,
    db:        Session = Depends(get_db),
    _:         User    = Depends(get_current_user),
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe