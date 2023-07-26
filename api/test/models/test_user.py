from app.models.user import UserDBSchema, UserSchema, UpdateUserSchema

# schemas


def test_user_schema():
    data = {
        "id": "64adf3d257736b2c0cd110f1",
        "username": "johndoe",
        "fullname": "John Doe",
        "email": "jdoe@x.edu.ng",
        "disabled": False,
    }
    user = UserSchema(**data)
    assert user.id == data["id"]
    assert user.username == data["username"]
    assert user.fullname == data["fullname"]
    assert user.email == data["email"]
    assert user.disabled == data["disabled"]


def test_user_db_schema():
    data = {
        "id": "64adf3d257736b2c0cd110f1",
        "username": "johndoe",
        "hashed_password": "64adf3d257736b2c0cd110f1",
        "fullname": "John Doe",
        "email": "jdoe@x.edu.ng",
        "disabled": False,
    }
    user = UserDBSchema(**data)
    assert user.id == data["id"]
    assert user.username == data["username"]
    assert user.hashed_password == data["hashed_password"]
    assert user.fullname == data["fullname"]
    assert user.email == data["email"]
    assert user.disabled == data["disabled"]


def test_update_user_schema():
    data = {
        "username": "johndoe_updated",
        "fullname": "John Doe Updated",
        "disabled": True,
    }
    user = UpdateUserSchema(**data)
    assert user.username == data["username"]
    assert user.fullname == data["fullname"]
    assert user.disabled == data["disabled"]


# helpers


def dict_to_user_db_schema(user: dict) -> UserDBSchema:
    return UserDBSchema(
        id=user["_id"],
        username=user["username"],
        hashed_password=user["hashed_password"],
        fullname=user["fullname"],
        email=user["email"],
        disabled=user["disabled"],
    )
