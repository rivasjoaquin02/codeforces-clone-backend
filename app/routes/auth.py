from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, ValidationError

from app.models.user import UserSchema, UserSignupSchema
from app.models.user_crud import add_user, retrieve_user
from app.utils.password_utils import verify_password

from app.utils.token import create_access_token


router = APIRouter()


class AditionalDataForm(BaseModel):
    email: EmailStr = Form()
    fullname: str = Form()


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class UserResponse(UserSchema):
    access_token: AccessToken


@router.post(
    "/signin",
    status_code=status.HTTP_200_OK,
    response_description="Sign In a user",
    response_model=UserResponse,
)
async def signin(form: OAuth2PasswordRequestForm = Depends()):
    user_in_db = await retrieve_user("username", form.username)
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user_in_db.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form.password, user_in_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(sub=form.username)
    return UserResponse(
        id=user_in_db.id,
        username=user_in_db.username,
        email=user_in_db.email,
        fullname=user_in_db.fullname,
        disabled=user_in_db.disabled,
        avatar=user_in_db.avatar,
        access_token=AccessToken(access_token=access_token, token_type="bearer"),
    )


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_description="Register a new user",
    response_model=UserResponse,
)
async def register(
    form: OAuth2PasswordRequestForm = Depends(),
    aditional: AditionalDataForm = Depends(),
):
    print (form.username, form.password, aditional.email, aditional.fullname)
    try:
        user_form = UserSignupSchema(
            username=form.username,
            password=form.password,
            email=aditional.email,
            fullname=aditional.fullname,
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())

    inserted_user = await add_user(user_form)
    if not inserted_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(sub=form.username)
    return UserResponse(
        id=inserted_user.id,
        username=inserted_user.username,
        email=inserted_user.email,
        fullname=inserted_user.fullname,
        disabled=inserted_user.disabled,
        avatar=inserted_user.avatar,
        access_token=AccessToken(access_token=access_token, token_type="bearer"),
    )
