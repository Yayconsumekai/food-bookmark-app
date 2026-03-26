from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.folder_service import (
    get_user_folders, create_folder, update_folder, delete_folder
)
from app.schemas.folder import FolderCreate, FolderUpdate, FolderOut
from typing import List

router = APIRouter(prefix="/api/folders", tags=["folders"])

@router.get("/", response_model=List[FolderOut])
def list_folders(
    db:   Session = Depends(get_db),
    user: User    = Depends(get_current_user),
):
    return get_user_folders(db, user.id)

@router.post("/", response_model=FolderOut, status_code=201)
def create(
    payload: FolderCreate,
    db:      Session = Depends(get_db),
    user:    User    = Depends(get_current_user),
):
    return create_folder(db, user.id, payload.name)

@router.put("/{folder_id}", response_model=FolderOut)
def update(
    folder_id: int,
    payload:   FolderUpdate,
    db:        Session = Depends(get_db),
    user:      User    = Depends(get_current_user),
):
    return update_folder(db, user.id, folder_id, payload.name)

@router.delete("/{folder_id}", status_code=204)
def delete(
    folder_id: int,
    db:        Session = Depends(get_db),
    user:      User    = Depends(get_current_user),
):
    delete_folder(db, user.id, folder_id)