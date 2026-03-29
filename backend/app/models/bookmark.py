from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"),   nullable=False)
    recipe_id  = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    folder_id  = Column(Integer, ForeignKey("folders.id"), nullable=False)
    rating     = Column(Float,   nullable=False, default=0)  # 1–5 stars
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # A user can only bookmark the same recipe once per folder
    __table_args__ = (
        UniqueConstraint("user_id", "recipe_id", "folder_id",
                         name="uq_user_recipe_folder"),
    )

    user    = relationship("User",   back_populates="bookmarks")
    folder  = relationship("Folder", back_populates="bookmarks")
    recipe  = relationship("Recipe")