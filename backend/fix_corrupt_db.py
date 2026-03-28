from app.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()
db.execute(text(
    "UPDATE recipes SET image_url = NULL "
    "WHERE image_url LIKE '%39c7f1ac414aff8e4ebfde26607fea68%'"
))
db.commit()
db.close()
print('Done — 2 corrupt DB rows cleaned up')