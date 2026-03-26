from pydantic import BaseModel
from typing import Optional

class RecipeCard(BaseModel):
    id:          int
    name:        str
    image_url:   Optional[str]
    category:    Optional[str]
    rating:      Optional[float]
    total_time:  Optional[str]
    calories:    Optional[float]

    class Config:
        from_attributes = True

class RecipeDetail(RecipeCard):
    description:  Optional[str]
    ingredients:  Optional[str]
    instructions: Optional[str]
    keywords:     Optional[str]