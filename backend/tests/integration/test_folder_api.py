import pytest

class TestFolderCRUD:
    def test_create_folder(self, client, auth_headers):
        response = client.post("/api/folders/", json={"name": "Favourites"},
                               headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["name"] == "Favourites"

    def test_list_folders_empty(self, client, auth_headers):
        response = client.get("/api/folders/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_list_folders_shows_created(self, client, auth_headers):
        client.post("/api/folders/", json={"name": "Breakfast"},
                    headers=auth_headers)
        response = client.get("/api/folders/", headers=auth_headers)
        names = [f["name"] for f in response.json()]
        assert "Breakfast" in names

    def test_duplicate_folder_name_fails(self, client, auth_headers):
        client.post("/api/folders/", json={"name": "Dinner"},
                    headers=auth_headers)
        response = client.post("/api/folders/", json={"name": "Dinner"},
                               headers=auth_headers)
        assert response.status_code == 400

    def test_update_folder_name(self, client, auth_headers):
        create = client.post("/api/folders/", json={"name": "Old Name"},
                             headers=auth_headers)
        folder_id = create.json()["id"]

        response = client.put(
            f"/api/folders/{folder_id}",
            json={"name": "New Name"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["name"] == "New Name"

    def test_delete_folder(self, client, auth_headers):
        create = client.post("/api/folders/", json={"name": "ToDelete"},
                             headers=auth_headers)
        folder_id = create.json()["id"]

        delete = client.delete(f"/api/folders/{folder_id}",
                               headers=auth_headers)
        assert delete.status_code == 204

        # Confirm it's gone
        response = client.get("/api/folders/", headers=auth_headers)
        names = [f["name"] for f in response.json()]
        assert "ToDelete" not in names

    def test_cannot_access_folders_without_auth(self, client):
        response = client.get("/api/folders/")
        assert response.status_code == 401

    def test_cannot_delete_other_users_folder(self, client, db, auth_headers):
        """User B should not be able to delete User A's folder."""
        from app.models.user   import User
        from app.models.folder import Folder
        from app.services.auth_service import hash_password

        # Create a second user and their folder
        user_b = User(username="userb", email="b@test.com",
                      password=hash_password("pass"))
        db.add(user_b)
        db.commit()

        folder = Folder(name="User B Folder", user_id=user_b.id)
        db.add(folder)
        db.commit()

        # User A tries to delete User B's folder
        response = client.delete(
            f"/api/folders/{folder.id}",
            headers=auth_headers,
        )
        assert response.status_code == 403