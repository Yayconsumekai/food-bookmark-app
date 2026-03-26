from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.models.folder   import Folder
from app.models.bookmark import Bookmark

def get_user_folders(db: Session, user_id: int) -> list:
    """Return all folders for a user with bookmark counts."""
    folders = db.query(Folder).filter(Folder.user_id == user_id).all()

    result = []
    for folder in folders:
        count = db.query(func.count(Bookmark.id))\
                  .filter(Bookmark.folder_id == folder.id)\
                  .scalar()
        result.append({
            "id":             folder.id,
            "name":           folder.name,
            "bookmark_count": count,
        })
    return result

def create_folder(db: Session, user_id: int, name: str) -> Folder:
    # Prevent duplicate folder names per user
    existing = db.query(Folder).filter(
        Folder.user_id == user_id,
        Folder.name    == name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Folder name already exists")

    folder = Folder(user_id=user_id, name=name)
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder

def update_folder(db: Session, user_id: int, folder_id: int, name: str) -> Folder:
    folder = _get_owned_folder(db, user_id, folder_id)
    folder.name = name
    db.commit()
    db.refresh(folder)
    return folder

def delete_folder(db: Session, user_id: int, folder_id: int):
    folder = _get_owned_folder(db, user_id, folder_id)
    db.delete(folder)   # cascades to bookmarks automatically
    db.commit()

def _get_owned_folder(db: Session, user_id: int, folder_id: int) -> Folder:
    """Fetch a folder and verify it belongs to the requesting user."""
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    if folder.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your folder")
    return folder