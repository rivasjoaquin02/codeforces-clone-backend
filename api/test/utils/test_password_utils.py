import random
from app.utils.password_utils import hash_password, verify_password


def test_hash_unhash_password():
    plain_password = f"secret{random.randint(0, 1000000)}"
    hashed_password = hash_password(plain_password)

    assert verify_password(plain_password, hashed_password) is True


def test_hash_unhash_false():
    plain_password = f"secret{random.randint(0, 1000000)}"
    hashed_password = hash_password(plain_password)
    assert verify_password("secret", hashed_password) is False
