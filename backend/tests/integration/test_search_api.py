import pytest
from sqlalchemy import text

class TestSearchEndpoint:
    def setup_method(self, db=None):
        pass

    def test_search_requires_auth(self, client):
        response = client.get("/api/search/", params={"q": "chicken"})
        assert response.status_code == 401

    def test_search_returns_results_structure(self, client, auth_headers,
                                          db, test_recipe):
        # Skip building tsvector — SQLite uses LIKE fallback, search_vector not needed
        response = client.get(
            "/api/search/",
            params={"q": "chicken"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total"   in data
        assert isinstance(data["results"], list)

    def test_search_empty_query_fails(self, client, auth_headers):
        response = client.get(
            "/api/search/",
            params={"q": ""},
            headers=auth_headers,
        )
        assert response.status_code == 422

    def test_get_recipe_by_id(self, client, auth_headers, test_recipe):
        response = client.get(
            f"/api/search/recipe/{test_recipe.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"]   == test_recipe.id
        assert data["name"] == test_recipe.name

    def test_get_nonexistent_recipe_returns_404(self, client, auth_headers):
        response = client.get(
            "/api/search/recipe/999888777",
            headers=auth_headers,
        )
        assert response.status_code == 404


class TestSpellCheckEndpoint:
    def test_spell_check_correct_word(self, client, auth_headers):
        response = client.get(
            "/api/search/spell-check",
            params={"q": "chicken"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "has_corrections" in data
        assert "corrected"       in data

    def test_spell_check_requires_auth(self, client):
        response = client.get(
            "/api/search/spell-check",
            params={"q": "chicken"},
        )
        assert response.status_code == 401