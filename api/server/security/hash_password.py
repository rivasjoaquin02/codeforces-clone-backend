from passlib.context import CryptContext


def hash_password(
        pwd_context: CryptContext,
        plain_password: str) -> str:
    return pwd_context.hash(plain_password)
