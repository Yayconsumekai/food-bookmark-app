"""
Retry caching images that previously failed.
Marks permanently dead URLs as NULL in the DB.
Run: python retry_images.py --limit 3000
"""
import asyncio
import argparse
import httpx
from pathlib import Path
from sqlalchemy import text
from app.database import SessionLocal
from app.models.recipe import Recipe
from app.services.image_service import cache_image

CACHE_DIR = Path("static/images")

async def is_url_alive(client: httpx.AsyncClient, url: str) -> bool:
    """Quick HEAD request to check if URL is reachable."""
    try:
        r = await client.head(url, timeout=6.0, follow_redirects=True)
        return r.status_code == 200
    except Exception:
        return False

async def run(limit: int):
    db = SessionLocal()

    # Get recipes with external (not yet cached) image URLs
    rows = db.execute(text("""
        SELECT id, image_url FROM recipes
        WHERE image_url IS NOT NULL
        AND image_url NOT LIKE '%/static/images/%'
        LIMIT :limit
    """), {"limit": limit}).fetchall()

    print(f"Retrying {len(rows)} uncached image URLs...")

    success      = 0
    dead         = 0
    batch_size   = 15

    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]

            # First check which URLs are alive (fast HEAD requests)
            alive_checks = await asyncio.gather(
                *[is_url_alive(client, row.image_url) for row in batch],
                return_exceptions=True
            )

            tasks = []
            live_rows = []
            dead_ids  = []

            for row, alive in zip(batch, alive_checks):
                if alive is True:
                    tasks.append(cache_image(row.image_url))
                    live_rows.append(row)
                else:
                    dead_ids.append(row.id)
                    dead += 1

            # Null out dead URLs so we never retry them
            if dead_ids:
                db.execute(text("""
                    UPDATE recipes SET image_url = NULL
                    WHERE id = ANY(:ids)
                """), {"ids": dead_ids})

            # Cache live images concurrently
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for row, result in zip(live_rows, results):
                    if result and not isinstance(result, Exception):
                        db.execute(text("""
                            UPDATE recipes SET image_url = :url WHERE id = :id
                        """), {"url": result["thumb"], "id": row.id})
                        success += 1
                    else:
                        # Failed to download even though URL appeared alive
                        db.execute(text(
                            "UPDATE recipes SET image_url = NULL WHERE id = :id"
                        ), {"id": row.id})
                        dead += 1

            db.commit()
            print(f"  {i + len(batch)}/{len(rows)} — "
                  f"✓ {success} cached, ✗ {dead} dead")

    db.close()
    print(f"\n✅ Done: {success} newly cached, {dead} dead URLs nulled out")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=3000)
    args = parser.parse_args()
    asyncio.run(run(args.limit))