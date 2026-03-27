from sqlalchemy import Column, Integer, String, Text, Float, ARRAY
from sqlalchemy import types
from app.database import Base
import os

# Custom type that acts as TSVECTOR on PostgreSQL, plain Text on SQLite
class TSVECTORType(types.TypeDecorator):
    impl = types.Text
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            from sqlalchemy.dialects.postgresql import TSVECTOR
            return dialect.type_descriptor(TSVECTOR())
        else:
            return dialect.type_descriptor(types.Text())

class Recipe(Base):
    __tablename__ = "recipes"

    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String, nullable=False, index=True)
    description     = Column(Text)
    instructions    = Column(Text)
    ingredients     = Column(Text)
    category        = Column(String)
    keywords        = Column(Text)
    image_url       = Column(String)
    rating          = Column(Float)
    total_time      = Column(String)
    calories        = Column(Float)

    # Works as TSVECTOR on PostgreSQL, Text on SQLite (tests)
    search_vector   = Column(TSVECTORType)