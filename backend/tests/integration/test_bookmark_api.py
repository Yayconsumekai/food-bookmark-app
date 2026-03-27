import pytest

@pytest.fixture()
def folder(client, auth_headers):
    """Helper: create a folder and return its data."""
    response = client.post("/api/folders/", json={"name": "Test Folder"},
                           headers=auth_headers)
    return response.json()

class TestBookmarkCRUD:
    def test_create_bookmark(self, client, auth_headers, folder, test_recipe):
        response = client.post("/api/bookmarks/", json={
            "recipe_id": test_recipe.id,
            "folder_id": folder["id"],
            "rating":    4.0,
        }, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["recipe_id"] == test_recipe.id
        assert data["rating"]    == 4.0

    def test_list_all_bookmarks(self, client, auth_headers,
                                folder, test_recipe):
        client.post("/api/bookmarks/", json={
            "recipe_id": test_recipe.id,
            "folder_id": folder["id"],
            "rating":    3.5,
        }, headers=auth_headers)

        response = client.get("/api/bookmarks/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_bookmarks_sorted_by_rating_descending(self, client,
                                                    auth_headers, db):
        from app.models.recipe import Recipe
        from app.models.folder import Folder
        from app.models.user   import User

        # Get the test user
        user = db.query(User).filter(User.email == "test@example.com").first()

        folder = Folder(name="Sort Test Folder", user_id=user.id)
        db.add(folder)

        r1 = Recipe(id=111111, name="Low Rated",  rating=2.0,
                    ingredients="a", instructions="a")
        r2 = Recipe(id=222222, name="High Rated", rating=5.0,
                    ingredients="b", instructions="b")
        db.add_all([r1, r2])
        db.commit()

        client.post("/api/bookmarks/", json={
            "recipe_id": 111111, "folder_id": folder.id, "rating": 2.0
        }, headers=auth_headers)
        client.post("/api/bookmarks/", json={
            "recipe_id": 222222, "folder_id": folder.id, "rating": 5.0
        }, headers=auth_headers)

        response = client.get("/api/bookmarks/", headers=auth_headers)
        ratings = [b["rating"] for b in response.json()]
        assert ratings == sorted(ratings, reverse=True)   # must be descending

    def test_duplicate_bookmark_fails(self, client, auth_headers,
                                      folder, test_recipe):
        client.post("/api/bookmarks/", json={
            "recipe_id": test_recipe.id,
            "folder_id": folder["id"],
            "rating":    3.0,
        }, headers=auth_headers)

        response = client.post("/api/bookmarks/", json={
            "recipe_id": test_recipe.id,
            "folder_id": folder["id"],
            "rating":    4.0,
        }, headers=auth_headers)
        assert response.status_code == 400

    def test_update_bookmark_rating(self, client, auth_headers,
                                    folder, test_recipe):
        create = client.post("/api/bookmarks/", json={
            "recipe_id": test_recipe.id,
            "folder_id": folder["id"],
            "rating":    3.0,
        }, headers=auth_headers)
        bookmark_id = create.json()["id"]

        response = client.put(
            f"/api/bookmarks/{bookmark_id}",
            json={"rating": 5.0},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["rating"] == 5.0

    def test_delete_bookmark(self, client, auth_headers,
                             folder, test_recipe):
        create = client.post("/api/bookmarks/", json={
            "recipe_id": test_recipe.id,
            "folder_id": folder["id"],
            "rating":    4.0,
        }, headers=auth_headers)
        bookmark_id = create.json()["id"]

        delete = client.delete(
            f"/api/bookmarks/{bookmark_id}",
            headers=auth_headers,
        )
        assert delete.status_code == 204

    def test_rating_must_be_between_1_and_5(self, client, auth_headers,
                                             folder, test_recipe):
        response = client.post("/api/bookmarks/", json={
            "recipe_id": test_recipe.id,
            "folder_id": folder["id"],
            "rating":    6.0,     # invalid
        }, headers=auth_headers)
        assert response.status_code == 422