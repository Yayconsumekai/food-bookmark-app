from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    username   = Column(String, unique=True, nullable=False, index=True)
    email      = Column(String, unique=True, nullable=False, index=True)
    password   = Column(String, nullable=False)    # hashed, never plain text
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    bookmarks  = relationship("Bookmark", back_populates="user")
    folders    = relationship("Folder",   back_populates="user")