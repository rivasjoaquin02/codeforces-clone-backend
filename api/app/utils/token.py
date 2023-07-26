from fastapi import HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta

# env variables
from dotenv import dotenv_values

env = dotenv_values(".env")
# SECRET_KEY = str(env.get("SECRET_KEY", "default_secret_key"))
# ALGORITHM = str(env.get("ALGORITHM", "default_algorithm"))
# TOKEN_EXPIRE_MINUTES = float(env.get("TOKEN_EXPIRE_MINUTES") or 30.0)
TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "8f09ecb804da72a44a4684c83a82172749600686e984dc79cb30e6aef6947eb4"
ALGORITHM = "HS256"


class Token(BaseModel):
    sub: str
    exp: str | datetime


def create_access_token(sub: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    # plain access_token
    access_token = Token(sub=sub, exp=exp)

    # encoded access_token
    try:
        token: str = token_encode(access_token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create access token",
        )

    return token


def token_encode(plain_token: Token) -> str:
    encoded_token: str = jwt.encode(plain_token.dict(), SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token


def token_decode(encoded_token: str) -> Token:
    plain_token = jwt.decode(encoded_token, SECRET_KEY, algorithms=[ALGORITHM])
    return Token(**plain_token)
