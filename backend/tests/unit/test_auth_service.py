import pytest
from app.services.auth_service import hash_password, verify_password, create_token
from jose import jwt
import os

class TestPasswordHashing:
    def test_hash_is_not_plain_text(self):
        hashed = hash_password("mypassword")
        assert hashed != "mypassword"

    def test_correct_password_verifies(self):
        hashed = hash_password("mypassword")
        assert verify_password("mypassword", hashed) is True

    def test_wrong_password_fails(self):
        hashed = hash_password("mypassword")
        assert verify_password("wrongpassword", hashed) is False

    def test_different_hashes_for_same_password(self):
        """bcrypt uses salt — same password should produce different hashes."""
        h1 = hash_password("mypassword")
        h2 = hash_password("mypassword")
        assert h1 != h2


class TestJWTToken:
    def test_token_contains_user_id(self):
        token = create_token({"sub": "42"})
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY", "changeme"),
            algorithms=["HS256"],
        )
        assert payload["sub"] == "42"

    def test_token_has_expiry(self):
        token = create_token({"sub": "1"})
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY", "changeme"),
            algorithms=["HS256"],
        )
        assert "exp" in payload

    def test_token_is_string(self):
        token = create_token({"sub": "1"})
        assert isinstance(token, str)
        assert len(token) > 10