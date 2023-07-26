from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError

from app.models.user import UserSchema
from app.models.user_crud import retrieve_user

from app.utils.token import token_decode


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
    # decode token
    try:
        payload = token_decode(token)
    except JWSError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    username = payload.sub
    user = await retrieve_user("username", username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    return user


async def current_active_user(user: UserSchema = Depends(current_user)) -> UserSchema:
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user"
        )
    return user
