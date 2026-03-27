from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.search_service import search_recipes
from app.services.spell_service import check_query
from app.services.image_service import cache_image, get_cached_url
from app.schemas.recipe import RecipeCard, RecipeDetail
from app.models.recipe import Recipe
import asyncio

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
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Build the response manually so validators fire correctly
    detail = RecipeDetail(
        id           = recipe.id,
        name         = recipe.name,
        image_url    = recipe.image_url,
        category     = recipe.category,
        rating       = recipe.rating,
        total_time   = recipe.total_time,
        calories     = recipe.calories,
        description  = recipe.description,
        keywords     = recipe.keywords,
        ingredients  = recipe.ingredients,
        instructions = recipe.instructions,
    )
    return detail

@router.get("/image-proxy")
async def image_proxy(
    url: str     = Query(...),
    db:  Session = Depends(get_db),
):
    """
    On-demand image proxy.
    Caches image locally on first request, then redirects to cached version.
    No auth required — images are public.
    """
    cached = get_cached_url(url, size="thumb")
    if cached != url:
        # Already cached — redirect to local copy
        return RedirectResponse(url=cached, status_code=301)

    # Not cached yet — download and cache now
    result = await cache_image(url)
    if result:
        # Update DB so future requests skip this
        db.query(Recipe).filter(Recipe.image_url == url).update({
            "image_url": result["thumb"]
        })
        db.commit()
        return RedirectResponse(url=result["thumb"], status_code=301)

    # Fallback — serve original URL
    return RedirectResponse(url=url, status_code=302)