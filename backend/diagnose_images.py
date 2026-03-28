"""
Diagnose image issues:
1. Cached WebP files that are corrupt or empty
2. DB rows still pointing to dead external URLs
3. DB rows pointing to local paths that don't exist on disk
"""
import asyncio
import httpx
from pathlib import Path
from sqlalchemy import text
from app.database import SessionLocal

CACHE_DIR = Path("static/images")

async def run():
    db = SessionLocal()

    print("=== Checking cached WebP files for corruption ===")
    webp_files  = list(CACHE_DIR.glob("*.webp"))
    empty       = [f for f in webp_files if f.stat().st_size < 1000]  # under 1KB = broken
    print(f"Total cached files : {len(webp_files)}")
    print(f"Corrupt/empty files: {len(empty)}")
    for f in empty[:5]:
        print(f"  - {f.name} ({f.stat().st_size} bytes)")

    print("\n=== Checking DB rows with external URLs (not yet cached) ===")
    rows = db.execute(text("""
        SELECT id, image_url FROM recipes
        WHERE image_url IS NOT NULL
        AND image_url NOT LIKE '%/static/images/%'
        LIMIT 20
    """)).fetchall()
    print(f"Recipes still pointing to external URLs: {len(rows)} (showing first 20)")

    print("\n=== Checking DB rows pointing to missing local files ===")
    local_rows = db.execute(text("""
        SELECT id, image_url FROM recipes
        WHERE image_url LIKE '%/static/images/%'
    """)).fetchall()

    missing = []
    for row in local_rows:
        filename = row.image_url.split("/static/images/")[-1]
        path     = CACHE_DIR / filename
        if not path.exists():
            missing.append(row)

    print(f"DB points to local file but file missing: {len(missing)}")
    for row in missing[:5]:
        print(f"  - Recipe {row.id}: {row.image_url}")

    print("\n=== Sampling 10 external URLs to check if alive ===")
    if rows:
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            for row in rows[:10]:
                try:
                    r = await client.head(row.image_url)
                    status = r.status_code
                except Exception as e:
                    status = f"ERROR: {e}"
                print(f"  {status} — {row.image_url[:80]}")

    db.close()

if __name__ == "__main__":
    asyncio.run(run())