from sqlalchemy import Column, Integer, String, Text, Float, ARRAY
from sqlalchemy.dialects.postgresql import TSVECTOR
from app.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String, nullable=False, index=True)
    description     = Column(Text)
    instructions    = Column(Text)          # joined steps
    ingredients     = Column(Text)          # joined ingredient list
    category        = Column(String)
    keywords        = Column(Text)
    image_url       = Column(String)        # first image from Images col
    rating          = Column(Float)
    total_time      = Column(String)
    calories        = Column(Float)

    # Full-text search vector — PostgreSQL built-in IR
    search_vector   = Column(TSVECTOR)