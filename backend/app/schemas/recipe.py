from pydantic import BaseModel, ConfigDict, model_validator
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

    model_config = ConfigDict(from_attributes=True)

class RecipeDetail(RecipeCard):
    description:       Optional[str] = None
    keywords:          Optional[str] = None
    ingredients:       Optional[str] = None
    instructions:      Optional[str] = None
    ingredients_list:  List[str] = []
    instructions_list: List[str] = []

    @model_validator(mode='after')
    def parse_lists(self):
        if self.ingredients:
            parts = re.split(r',\s*|\s{2,}', self.ingredients.strip())
            self.ingredients_list = [p.strip() for p in parts if p.strip()]
        if self.instructions:
            parts = re.split(r'\d+\.\s+|\s{2,}', self.instructions.strip())
            self.instructions_list = [p.strip() for p in parts if p.strip()]
        return self