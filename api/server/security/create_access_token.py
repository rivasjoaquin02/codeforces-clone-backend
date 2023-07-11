
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import JWTError, jwt


from server.db.models.user import ErrorResponseModel


def create_access_token(
        secretkey: str,
        algorithm: str,
        sub: str,
        duration_minutes: int = 15) -> str | HTTPException:

    exp = datetime.utcnow() + timedelta(minutes=duration_minutes)

    # plain access_token
    access_token = {"sub": sub, "exp": exp}

    # encoded access_token
    try:
        token = jwt.encode(access_token, secretkey, algorithm=algorithm)
    except JWTError:
        return ErrorResponseModel(
            code=status.HTTP_400_BAD_REQUEST,
            message="Error while creating the token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return token
