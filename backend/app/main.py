from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, search, folders, bookmarks

app = FastAPI(title="Food Bookmark API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(search.router)
app.include_router(folders.router)
app.include_router(bookmarks.router)

@app.get("/health")
def health():
    return {"status": "ok"}