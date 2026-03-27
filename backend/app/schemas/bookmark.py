from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.schemas.recipe import RecipeCard

class BookmarkCreate(BaseModel):
    recipe_id: int
    folder_id: int
    rating:    float = Field(..., ge=1, le=5)

class BookmarkUpdate(BaseModel):
    rating:    Optional[float] = Field(None, ge=1, le=5)
    folder_id: Optional[int]   = None

class BookmarkOut(BaseModel):
    id:        int
    recipe_id: int
    folder_id: int
    rating:    float
    recipe:    Optional[RecipeCard] = None

    model_config = ConfigDict(from_attributes=True)