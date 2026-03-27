"""
Run this script once after ingestion to pre-cache all recipe images.
Usage: python cache_images.py --limit 5000
"""
import asyncio
import argparse
import sys
from sqlalchemy import text
from app.database import SessionLocal
from app.services.image_service import cache_image
from app.models.recipe import Recipe

async def run(limit: int):
    db = SessionLocal()
    print(f"Fetching up to {limit} recipe image URLs...")

    recipes = (
        db.query(Recipe.id, Recipe.image_url)
        .filter(Recipe.image_url.isnot(None))
        .limit(limit)
        .all()
    )

    print(f"Caching {len(recipes)} images...")
    success = 0
    failed  = 0

    # Process in batches of 20 concurrent requests
    batch_size = 20
    for i in range(0, len(recipes), batch_size):
        batch = recipes[i:i + batch_size]
        tasks = [cache_image(r.image_url) for r in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for r, result in zip(batch, results):
            if result and not isinstance(result, Exception):
                # Update DB with cached thumb URL
                db.query(Recipe).filter(Recipe.id == r.id).update({
                    "image_url": result["thumb"]
                })
                success += 1
            else:
                failed += 1

        db.commit()
        pct = round((i + len(batch)) / len(recipes) * 100)
        print(f"  {i + len(batch)}/{len(recipes)} ({pct}%) — "
              f"✓ {success} cached, ✗ {failed} failed")

    db.close()
    print(f"\n✅ Done. {success} images cached, {failed} failed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=2000,
                        help="Number of images to cache (default: 2000)")
    args = parser.parse_args()
    asyncio.run(run(args.limit))