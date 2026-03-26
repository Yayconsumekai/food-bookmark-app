from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from fastapi import HTTPException
from app.models.bookmark import Bookmark
from app.models.folder   import Folder
from app.models.recipe   import Recipe

def get_all_bookmarks(db: Session, user_id: int) -> list:
    """
    Return all bookmarks for a user across all folders,
    sorted by the user's rating descending.
    """
    bookmarks = (
        db.query(Bookmark)
        .options(joinedload(Bookmark.recipe))
        .filter(Bookmark.user_id == user_id)
        .order_by(Bookmark.rating.desc())
        .all()
    )
    return bookmarks

def get_folder_bookmarks(db: Session, user_id: int, folder_id: int) -> list:
    """Return bookmarks in a specific folder, sorted by rating."""
    _verify_folder_ownership(db, user_id, folder_id)
    return (
        db.query(Bookmark)
        .options(joinedload(Bookmark.recipe))
        .filter(
            Bookmark.user_id  == user_id,
            Bookmark.folder_id == folder_id,
        )
        .order_by(Bookmark.rating.desc())
        .all()
    )

def create_bookmark(
    db:        Session,
    user_id:   int,
    recipe_id: int,
    folder_id: int,
    rating:    float,
) -> Bookmark:
    _verify_folder_ownership(db, user_id, folder_id)

    # Check recipe exists
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Check for duplicate
    existing = db.query(Bookmark).filter(
        Bookmark.user_id   == user_id,
        Bookmark.recipe_id == recipe_id,
        Bookmark.folder_id == folder_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already bookmarked in this folder")

    bookmark = Bookmark(
        user_id=user_id, recipe_id=recipe_id,
        folder_id=folder_id, rating=rating
    )
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark

def update_bookmark(
    db:          Session,
    user_id:     int,
    bookmark_id: int,
    rating:      float = None,
    folder_id:   int   = None,
) -> Bookmark:
    bookmark = _get_owned_bookmark(db, user_id, bookmark_id)

    if rating    is not None: bookmark.rating    = rating
    if folder_id is not None:
        _verify_folder_ownership(db, user_id, folder_id)
        bookmark.folder_id = folder_id

    db.commit()
    db.refresh(bookmark)
    return bookmark

def delete_bookmark(db: Session, user_id: int, bookmark_id: int):
    bookmark = _get_owned_bookmark(db, user_id, bookmark_id)
    db.delete(bookmark)
    db.commit()

def _get_owned_bookmark(db: Session, user_id: int, bookmark_id: int) -> Bookmark:
    bookmark = db.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    if bookmark.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your bookmark")
    return bookmark

def _verify_folder_ownership(db: Session, user_id: int, folder_id: int):
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    if folder.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your folder")