import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Use SQLite in-memory DB for testing — never touches real PostgreSQL
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables before tests, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db():
    """Provide a test DB session that rolls back after each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(db):
    """Provide a test HTTP client with DB overridden."""
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture()
def test_user(db):
    """Create a test user and return their data."""
    from app.models.user import User
    from app.services.auth_service import hash_password
    user = User(
        username="testuser",
        email="test@example.com",
        password=hash_password("password123"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture()
def auth_headers(client, test_user):
    """Log in and return Authorization headers."""
    response = client.post("/api/auth/login", json={
        "email":    "test@example.com",
        "password": "password123",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture()
def test_recipe(db):
    """Create a test recipe for use in other tests."""
    from app.models.recipe import Recipe
    recipe = Recipe(
        id=999999,
        name="Test Chicken Soup",
        description="A warm comforting soup",
        ingredients="chicken garlic onion salt pepper",
        instructions="Boil chicken Add vegetables Simmer",
        category="Soups",
        keywords="chicken soup warm comfort",
        image_url=None,
        rating=4.5,
        total_time="1h 30m",
        calories=320.0,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe