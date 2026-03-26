from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FolderCreate(BaseModel):
    name: str

class FolderUpdate(BaseModel):
    name: str

class FolderOut(BaseModel):
    id:             int
    name:           str
    bookmark_count: Optional[int] = 0   # populated in service layer

    class Config:
        from_attributes = True