from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.bookmark_service import (
    get_all_bookmarks, get_folder_bookmarks,
    create_bookmark, update_bookmark, delete_bookmark
)
from app.schemas.bookmark import BookmarkCreate, BookmarkUpdate, BookmarkOut

router = APIRouter(prefix="/api/bookmarks", tags=["bookmarks"])

@router.get("/", response_model=List[BookmarkOut])
def list_all(
    db:   Session = Depends(get_db),
    user: User    = Depends(get_current_user),
):
    """All bookmarks across all folders, sorted by rating."""
    return get_all_bookmarks(db, user.id)

@router.get("/folder/{folder_id}", response_model=List[BookmarkOut])
def list_by_folder(
    folder_id: int,
    db:        Session = Depends(get_db),
    user:      User    = Depends(get_current_user),
):
    return get_folder_bookmarks(db, user.id, folder_id)

@router.post("/", response_model=BookmarkOut, status_code=201)
def create(
    payload: BookmarkCreate,
    db:      Session = Depends(get_db),
    user:    User    = Depends(get_current_user),
):
    return create_bookmark(
        db, user.id,
        payload.recipe_id,
        payload.folder_id,
        payload.rating,
    )

@router.put("/{bookmark_id}", response_model=BookmarkOut)
def update(
    bookmark_id: int,
    payload:     BookmarkUpdate,
    db:          Session = Depends(get_db),
    user:        User    = Depends(get_current_user),
):
    return update_bookmark(
        db, user.id, bookmark_id,
        rating=payload.rating,
        folder_id=payload.folder_id,
    )

@router.delete("/{bookmark_id}", status_code=204)
def delete(
    bookmark_id: int,
    db:          Session  = Depends(get_db),
    user:        User     = Depends(get_current_user),
):
    delete_bookmark(db, user.id, bookmark_id)