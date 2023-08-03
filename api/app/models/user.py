from pydantic import BaseModel, EmailStr, Field

# schemas


class UserSchema(BaseModel):
    id: str
    username: str = Field(..., min_length=3, max_length=20)
    fullname: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    disabled: bool
    avatar: str

    class Config:
        schema_extra = {
            "example": {
                "id": "64adf3d257736b2c0cd110f1",
                "username": "johndoe",
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "disabled": False,
            }
        }


class UpdateUserSchema(BaseModel):
    username: str | None
    password: str | None
    fullname: str | None
    email: EmailStr | None
    disabled: bool | None

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoeNew",
            }
        }


class UserDBSchema(UserSchema):
    hashed_password: str


class UserSignupSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    fullname: str = Field(..., min_length=3, max_length=50)

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "secret",
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
            }
        }


# helpers


def dict_to_user_schema(user: dict) -> UserSchema:
    return UserSchema(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"],
        fullname=user["fullname"],
        disabled=user["disabled"],
        avatar=user["avatar"],
    )


def dict_to_user_db_schema(user: dict) -> UserDBSchema:
    return UserDBSchema(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"],
        fullname=user["fullname"],
        disabled=user["disabled"],
        hashed_password=user["hashed_password"],
        avatar=user["avatar"],
    )
