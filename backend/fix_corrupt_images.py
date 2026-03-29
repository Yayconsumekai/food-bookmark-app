"""
Delete corrupt cached images and null-out their DB URLs
so the frontend shows the fallback emoji instead of a broken image.
"""
from pathlib import Path
from sqlalchemy import text
from app.database import SessionLocal

CACHE_DIR    = Path("static/images")
MIN_SIZE     = 1000   # anything under 1KB is considered corrupt

def run():
    db    = SessionLocal()
    files = list(CACHE_DIR.glob("*.webp"))

    corrupt  = [f for f in files if f.stat().st_size < MIN_SIZE]
    print(f"Found {len(corrupt)} corrupt files out of {len(files)} total")

    deleted = 0
    for f in corrupt:
        print(f"  Deleting {f.name} ({f.stat().st_size} bytes)")
        f.unlink()
        deleted += 1

    # Null out DB rows that pointed to these deleted files
    # so they don't try to load a 404 path
    print("\nNulling out DB image_url for deleted files...")
    db.execute(text("""
        UPDATE recipes
        SET image_url = NULL
        WHERE image_url LIKE '%/static/images/%'
        AND id IN (
            SELECT r.id FROM recipes r
            WHERE NOT EXISTS (
                SELECT 1 FROM (
                    SELECT SUBSTRING(image_url FROM '.*/(.+)$') AS fname
                    FROM recipes
                    WHERE image_url LIKE '%/static/images/%'
                ) sub
            )
        )
    """))

    # Simpler approach — check each file directly
    local_rows = db.execute(text("""
        SELECT id, image_url FROM recipes
        WHERE image_url LIKE '%/static/images/%'
    """)).fetchall()

    nulled = 0
    for row in local_rows:
        filename = row.image_url.split("/static/images/")[-1]
        path     = CACHE_DIR / filename
        if not path.exists():
            db.execute(text(
                "UPDATE recipes SET image_url = NULL WHERE id = :id"
            ), {"id": row.id})
            nulled += 1

    db.commit()
    db.close()
    print(f"✅ Deleted {deleted} corrupt files, nulled {nulled} DB rows")
    print("Frontend will now show 🍽️ fallback for these recipes")

if __name__ == "__main__":
    run()