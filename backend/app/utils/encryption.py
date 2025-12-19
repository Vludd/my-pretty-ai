from hashlib import sha256

from passlib.hash import argon2


def get_password_hash(password: str) -> str:
    return argon2.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return argon2.verify(plain_password, hashed_password)

def hash_recovery_key(key: str) -> str:
    return sha256(key.encode()).hexdigest()

def verify_recovery_key(input_key: str, stored_hash: str) -> bool:
    return sha256(input_key.encode()).hexdigest() == stored_hash
