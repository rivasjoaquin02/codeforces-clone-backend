
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field

# user without password


class UserSchema(BaseModel):
    id: str
    username: str = Field(...)
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    disabled: bool

    class Config:
        schema_extra = {
            "example": {
                "id": "",
                "username": "johndoe",
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "disabled": False
            }
        }

class UpdateUserSchema(BaseModel):
    username: str | None = None
    fullname: str | None = None
    email: EmailStr | None = None
    disabled: bool | None = None

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe_new",
            }
        }

# user in db

class UserDBSchema(UserSchema):
    hashed_password: str


class SignUpUserSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    fullname: str | None = Field()
    email: EmailStr = Field(...)


def ResponseModel(data, message: str) -> dict:
    return {
        "data": [data],
        "message": message
    }


def ErrorResponseModel(
        code: int,
        message: str,
        headers: dict | None = None) -> HTTPException:
    return HTTPException(
        status_code=code,
        detail=message,
        headers=headers
    )
