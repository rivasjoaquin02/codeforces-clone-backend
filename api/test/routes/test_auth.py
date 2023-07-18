from app.app import app

from fastapi import status
from fastapi.testclient import TestClient

from app.db.database import client as db_client

client = TestClient(app)
users_collection = db_client.users.get_collection("users_collection")


def clean_user(id: str) -> dict:
    deleted_user: dict = users_collection.delete_one({"_id": id})
    return deleted_user


def test_signup_0():
    data = {
        "username": "johndoe",
        "password": "secret",
        "email": "johndoe@email.com",
        "fullname": "John Doe",
    }

    response = client.post(
        "/auth/signup",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["sub"] is not None
    assert response.json()["exp"] is not None

    inserted_user: dict = users_collection.find_one({"username": "johndoe"})
    assert inserted_user is not None

    # clean
    assert clean_user(inserted_user["_id"]) is not None
