import httpx
import hashlib
import os
import logging
from pathlib import Path
from PIL import Image
import io
import os

logger     = logging.getLogger(__name__)
CACHE_DIR  = Path("static/images")
BASE_URL = os.getenv("IMAGE_BASE_URL", "http://localhost:8000/static/images")

# Sizes to generate
SIZES = {
    "thumb": 300,   # used in cards
    "full":  800,   # used in modal hero
}

def _url_to_filename(url: str, suffix: str) -> str:
    """Generate a stable filename from a URL using its hash."""
    h = hashlib.md5(url.encode()).hexdigest()
    return f"{h}_{suffix}.webp"

def _is_cached(url: str) -> dict | None:
    """Check if both sizes are already cached. Return paths if so."""
    thumb_name = _url_to_filename(url, "thumb")
    full_name  = _url_to_filename(url, "full")

    thumb_path = CACHE_DIR / thumb_name
    full_path  = CACHE_DIR / full_name

    if thumb_path.exists() and full_path.exists():
        return {
            "thumb": f"{BASE_URL}/{thumb_name}",
            "full":  f"{BASE_URL}/{full_name}",
        }
    return None


async def cache_image(url: str) -> dict | None:
    """
    Download, resize, and cache an image.
    Returns dict with 'thumb' and 'full' local URLs, or None on failure.
    """
    if not url:
        return None

    # Check cache first
    cached = _is_cached(url)
    if cached:
        return cached

    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(url)
            if response.status_code != 200:
                return None

            img_data = response.content
            img      = Image.open(io.BytesIO(img_data)).convert("RGB")

            result = {}
            for size_name, max_px in SIZES.items():
                # Resize maintaining aspect ratio
                img_copy = img.copy()
                img_copy.thumbnail((max_px, max_px), Image.LANCZOS)

                filename = _url_to_filename(url, size_name)
                out_path = CACHE_DIR / filename

                # Save as WebP with quality optimization
                img_copy.save(
                    out_path,
                    format="WEBP",
                    quality=82,
                    method=6,       # slower encode, better compression
                )
                result[size_name] = f"{BASE_URL}/{filename}"

            return result

    except Exception as e:
        logger.warning(f"Failed to cache image {url}: {e}")
        return None


def get_cached_url(url: str, size: str = "thumb") -> str:
    """
    Synchronous version — returns cached URL if exists,
    otherwise returns original URL as fallback.
    """
    if not url:
        return url
    cached = _is_cached(url)
    if cached:
        return cached.get(size, url)
    return url   # fallback to original