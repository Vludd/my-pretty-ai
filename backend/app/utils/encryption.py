from passlib.hash import argon2


def get_password_hash(password: str) -> str:
    return argon2.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return argon2.verify(plain_password, hashed_password)
