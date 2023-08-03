from fastapi import HTTPException, status

# db client
from app.db.database import client

# models
from app.models.user import (
    UserSchema,
    UpdateUserSchema,
    UserDBSchema,
    UserSignupSchema,
    dict_to_user_schema,
    dict_to_user_db_schema,
)

from bson import ObjectId

# utils
from app.utils.password_utils import hash_password

users_collection = client.users.get_collection("users_collection")


async def retrieve_users() -> list[UserSchema]:
    """
    Retrieve all users present in the database
    """
    users = []
    async for user in users_collection.find():
        users.append(dict_to_user_schema(user))
    return users


async def retrieve_user(field: str, key: str | ObjectId) -> UserDBSchema | None:
    """
    example:
    retrieve_user(field="username", key="johndoe") -> dict
    """
    user_in_db = await users_collection.find_one({field: key})

    if not user_in_db:
        return None

    return dict_to_user_db_schema(user_in_db)


async def add_user(user_data: UserSignupSchema) -> UserDBSchema | None:
    """
    Add a new user into to the database
    """

    user_in_db = await retrieve_user(
        "username", user_data.username
    ) or await retrieve_user("email", user_data.email)

    # print ("---->" , user_in_db)

    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or Email already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_to_insert = {
        "username": user_data.username,
        "fullname": user_data.fullname,
        "email": user_data.email,
        "hashed_password": hash_password(user_data.password),
        "disabled": False,
        "avatar": "avatar",
    }

    inserted_user = await users_collection.insert_one(user_to_insert)
    inserted_id: str = inserted_user.inserted_id
    user_in_db = await retrieve_user("_id", ObjectId(inserted_id))
    return user_in_db


async def update_user(id: str, user_data: UpdateUserSchema) -> UserSchema:
    """
    Update a user with a matching ID
    """
    user_in_db = await retrieve_user("_id", ObjectId(id))
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # remove None values
    user_to_update = {k: v for k, v in user_data.dict().items() if v is not None}

    if "password" in user_to_update:
        password = user_to_update.pop("password")
        user_to_update["hashed_password"] = hash_password(password)

    updated_user = await users_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": user_to_update}
    )

    if updated_user.modified_count > 0:
        user_in_db = await retrieve_user("_id", ObjectId(id))
        if user_in_db:
            return user_in_db

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Error no new info to update..."
    )


async def delete_user(id: str) -> UserSchema:
    """
    Delete a user with a matching ID
    """
    # user_in_db = await retrieve_user("_id", ObjectId(id))
    user_in_db = await users_collection.find_one({"_id": ObjectId(id)})

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    deleted_user: dict = await users_collection.delete_one({"_id": ObjectId(id)})
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not deleted"
        )

    return dict_to_user_schema(user_in_db)
