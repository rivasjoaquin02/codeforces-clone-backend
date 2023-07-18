from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    hashed_password: str = pwd_context.hash(plain_password)
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    same: bool = pwd_context.verify(plain_password, hashed_password)
    return same
