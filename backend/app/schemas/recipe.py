from pydantic import BaseModel, field_validator
from typing import Optional, List
import re

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
    description:       Optional[str]
    keywords:          Optional[str]
    ingredients_list:  List[str] = []
    instructions_list: List[str] = []

    # Raw DB fields — we parse them into lists
    ingredients:  Optional[str] = None
    instructions: Optional[str] = None

    @field_validator('ingredients_list', mode='before')
    @classmethod
    def parse_ingredients(cls, v, info):
        raw = info.data.get('ingredients', '')
        if not raw:
            return []
        # Split on comma or multiple spaces
        parts = re.split(r',\s*|\s{2,}', raw.strip())
        return [p.strip() for p in parts if p.strip()]

    @field_validator('instructions_list', mode='before')
    @classmethod
    def parse_instructions(cls, v, info):
        raw = info.data.get('instructions', '')
        if not raw:
            return []
        # Split on numbered steps or double spaces
        parts = re.split(r'\d+\.\s+|\s{2,}', raw.strip())
        return [p.strip() for p in parts if p.strip()]