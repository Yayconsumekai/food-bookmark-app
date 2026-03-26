import pandas as pd
import ast
import re
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal, engine
from app.models.recipe import Recipe
from app.database import Base

# ── helpers ──────────────────────────────────────────────────────────────────

def parse_list_field(value):
    """Safely parse R-style or Python-style list strings."""
    if pd.isna(value):
        return ""
    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, list):
            return " ".join(str(v) for v in parsed)
    except Exception:
        pass
    # fallback: strip c("...") R format
    cleaned = re.sub(r'^c\(|\)$', '', str(value))
    cleaned = re.sub(r'"', '', cleaned)
    return cleaned.replace(",", " ")

def extract_first_image(value):
    """Pull the first URL from the Images column."""
    if pd.isna(value):
        return None
    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, list) and parsed:
            return parsed[0]
    except Exception:
        pass
    match = re.search(r'https?://\S+', str(value))
    return match.group(0) if match else None

def clean_time(value):
    """Convert ISO duration like PT1H30M to readable string."""
    if pd.isna(value):
        return None
    s = str(value)
    hours = re.search(r'(\d+)H', s)
    mins  = re.search(r'(\d+)M', s)
    parts = []
    if hours: parts.append(f"{hours.group(1)}h")
    if mins:  parts.append(f"{mins.group(1)}m")
    return " ".join(parts) if parts else None

# ── main ingestion ────────────────────────────────────────────────────────────

def ingest(limit: int = None):
    print("Reading CSV...")
    df = pd.read_csv('../data/recipes.csv')

    if limit:
        df = df.head(limit)

    print(f"Processing {len(df)} recipes...")

    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    batch = []
    for i, row in df.iterrows():
        ingredients  = parse_list_field(row.get('RecipeIngredientParts'))
        instructions = parse_list_field(row.get('RecipeInstructions'))

        recipe = Recipe(
            id           = int(row['RecipeId']),
            name         = str(row.get('Name', '')),
            description  = str(row.get('Description', '')),
            instructions = instructions,
            ingredients  = ingredients,
            category     = str(row.get('RecipeCategory', '')),
            keywords     = parse_list_field(row.get('Keywords')),
            image_url    = extract_first_image(row.get('Images')),
            rating       = float(row['AggregatedRating']) if pd.notna(row.get('AggregatedRating')) else None,
            total_time   = clean_time(row.get('TotalTime')),
            calories     = float(row['Calories']) if pd.notna(row.get('Calories')) else None,
        )
        batch.append(recipe)

        # commit in batches of 1000 to avoid memory issues
        if len(batch) >= 1000:
            db.bulk_save_objects(batch)
            db.commit()
            batch = []
            print(f"  Committed {i+1} rows...")

    if batch:
        db.bulk_save_objects(batch)
        db.commit()

    print("Building full-text search vectors...")
    db.execute(text("""
        UPDATE recipes SET search_vector =
            setweight(to_tsvector('english', coalesce(name, '')), 'A') ||
            setweight(to_tsvector('english', coalesce(ingredients, '')), 'B') ||
            setweight(to_tsvector('english', coalesce(instructions, '')), 'C') ||
            setweight(to_tsvector('english', coalesce(description, '')), 'C')
    """))
    db.commit()

    print("Creating GIN index on search_vector...")
    db.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_recipes_search
        ON recipes USING GIN(search_vector)
    """))
    db.commit()

    db.close()
    print("✅ Done! Dataset loaded and indexed.")

if __name__ == "__main__":
    ingest()   # remove limit to load all ~500k rows (takes ~5-10 min)