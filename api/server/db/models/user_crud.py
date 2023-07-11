
from fastapi import status
from fastapi.encoders import jsonable_encoder

from server.security.hash_password import hash_password
from passlib.context import CryptContext

from server.db.models.user import (
    ErrorResponseModel,
    SignUpUserSchema,
    UpdateUserSchema,
    UserSchema)
from server.db.database import client
from bson.objectid import ObjectId


users_collection = client.users.get_collection("users_collection")


# CRUD


async def retrieve_users() -> list:
    '''
    Retrieve all users present in the database
    '''
    users = []
    async for user in users_collection.find():
        users.append(user)
    return users


async def retrieve_user(field: str, key: str | ObjectId) -> dict | None:
    '''
    example:
    retrieve_user(field="username", key="johndoe") -> dict
    '''
    user = await users_collection.find_one({field: key})
    return user


async def add_user(
    pwd_context: CryptContext,
    user_data: SignUpUserSchema
) -> dict | None:
    '''
    Add a new user into to the database
    '''

    exist = await retrieve_user("username", user_data.username)

    if not exist:
        # pydantic -> dict
        plain_user_data = {
            "username": user_data.username,
            "hashed_password": hash_password(pwd_context, user_data.password),
            "email": user_data.email,
            "fullname": user_data.fullname,
            "disabled": False
        }

        user = await users_collection.insert_one(plain_user_data)
        inserted_user = await retrieve_user("_id", user.inserted_id)
        return inserted_user


async def update_user(id: str, user_data: UpdateUserSchema) -> UserSchema | bool:
    '''
    Update a user with a matching ID
    '''
    empty = UpdateUserSchema()
    if user_data == empty:
        return False

    user = await retrieve_user("_id", ObjectId(id))
    if user:
        plain_user_data = jsonable_encoder(user_data)
        plain_user_data = {k: v
                           for k, v in plain_user_data.items()
                           if v is not None}

        updated_user = await users_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": plain_user_data}
        )
        if updated_user.modified_count > 0:
            user = await users_collection.find_one({"_id": ObjectId(id)})
            return UserSchema(
                id=str(user["_id"]),
                username=user["username"],
                email=user["email"],
                fullname=user["fullname"],
                disabled=user["disabled"],
            )
        raise ErrorResponseModel(
            code=status.HTTP_403_FORBIDDEN,
            message="Error no new info to update..."
        )
    return False


async def delete_user(id: str) -> bool:
    '''
    Delete a user with a matching ID
    '''
    user = await retrieve_user("_id", ObjectId(id))
    if user:
        await users_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False
