from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles        # ← add
from app.api import auth, search, folders, bookmarks, recommendations
from app.database import SessionLocal
from app.services.ml_suggestion_service import _build_tfidf_corpus
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Food Bookmark API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve cached images as static files
os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")  # ← add

app.include_router(auth.router)
app.include_router(search.router)
app.include_router(folders.router)
app.include_router(bookmarks.router)
app.include_router(recommendations.router)

@app.on_event("startup")
async def startup_event():
    """Pre-build the TF-IDF matrix when the server starts."""
    logger.info("Pre-building TF-IDF matrix on startup...")
    db = SessionLocal()
    try:
        _build_tfidf_corpus(db)
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}