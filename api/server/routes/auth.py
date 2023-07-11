
from fastapi import APIRouter, Body, Depends, Form, status
from pydantic.dataclasses import dataclass
from pydantic import EmailStr

# security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from server.security.create_access_token import create_access_token

# models
from server.db.models.user import (
    ErrorResponseModel,
    ResponseModel,
    SignUpUserSchema,
    UpdateUserSchema,
    UserSchema)
from server.db.models.user_crud import add_user, delete_user, retrieve_user, update_user


TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "8f09ecb804da72a44a4684c83a82172749600686e984dc79cb30e6aef6947eb4"
ALGORITHM = "HS256"


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token")  # TODO: can be url: token??
pwd_context = CryptContext(schemes=["bcrypt"])


async def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> UserSchema:
    credentials_exception = ErrorResponseModel(
        code=status.HTTP_401_UNAUTHORIZED,
        message="Could not validate credentials"
    )

    # decode token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # get the user from db
    user = await retrieve_user("username", username)
    if not user:
        raise credentials_exception

    return UserSchema(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"],
        fullname=user["fullname"],
        disabled=user["disabled"],
    )


async def get_current_active_user(
        current_user: UserSchema = Depends(get_current_user)
) -> UserSchema:
    if current_user.disabled:
        raise ErrorResponseModel(
            code=status.HTTP_401_UNAUTHORIZED,
            message="You're currently loggin"
        )
    return current_user


# SignIn

@dataclass
class AditionalDataForm:
    email: EmailStr = Form()
    fullname: str | None = Form(None)


@router.post("/signin",
             status_code=status.HTTP_201_CREATED,
             response_description="Sign In a new user")
async def signup(
        form: OAuth2PasswordRequestForm = Depends(),
        aditional: AditionalDataForm = Depends()):

    user_data = SignUpUserSchema(
        username=form.username,
        password=form.password,
        email=aditional.email,
        fullname=aditional.fullname
    )

    user = await add_user(pwd_context, user_data)

    if not user:
        raise ErrorResponseModel(code=status.HTTP_400_BAD_REQUEST,
                                 message="Username already exist",
                                 headers={"WWW-Authenticate": "Bearer"})

    access_token = create_access_token(
        secretkey=SECRET_KEY,
        algorithm=ALGORITHM,
        sub=user_data.username,
        duration_minutes=TOKEN_EXPIRE_MINUTES)

    return ResponseModel(data={"access_token": access_token, "token_type": "bearer"},
                         message="User correctly register...")


# Log In

@router.post("/login",
             status_code=status.HTTP_202_ACCEPTED,
             response_description="Log in user")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user = await retrieve_user("username", form.username)

    credentials_exception = ErrorResponseModel(code=status.HTTP_400_BAD_REQUEST,
                                               message="Incorrect username of password",
                                               headers={"WWW-Authenticate": "Bearer"})

    if not user:
        raise credentials_exception

    if not pwd_context.verify(form.password, user["hashed_password"]):
        raise credentials_exception

    access_token = create_access_token(
        secretkey=SECRET_KEY,
        algorithm=ALGORITHM,
        sub=form.username,
        duration_minutes=TOKEN_EXPIRE_MINUTES)

    return ResponseModel(data={"access_token": access_token, "token_type": "bearer"},
                         message="User correctly logged...")


# get user info

@router.get("/users/me",
            status_code=status.HTTP_200_OK,
            response_description="Retrieves the current user if loggin")
async def get_user(current_user: UserSchema = Depends(get_current_active_user)):
    return ResponseModel(
        data=current_user,
        message="User retreval correctly"
    )

# update user info


@router.put("/users/me",
            status_code=status.HTTP_206_PARTIAL_CONTENT,
            response_description="Updates the user info")
async def update_user_data(
        current_user: UserSchema = Depends(get_current_active_user),
        user_data: UpdateUserSchema = Body()):
    credentials_exception = ErrorResponseModel(code=status.HTTP_400_BAD_REQUEST,
                                               message="Incorrect username of password",
                                               headers={"WWW-Authenticate": "Bearer"})

    updated_user = await update_user(current_user.id, user_data)
    if updated_user is False:
        raise credentials_exception

    return ResponseModel(
        data=updated_user,
        message="User info correctly updated..."
    )


# delete user

@router.delete("/users/me",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Deletes the current user")
async def delete_user_data(current_user: UserSchema = Depends(get_current_active_user)):

    deleted_user = await delete_user(current_user.id)
    if not deleted_user:
        raise ErrorResponseModel(code=status.HTTP_400_BAD_REQUEST,
                                 message="User could not be deleted...",
                                 headers={"WWW-Authenticate": "Bearer"})
