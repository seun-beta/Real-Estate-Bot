from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from app.config import settings
from users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(
            minutes=settings.jwt_access_token_exp_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def get_user(email: str):
    return User.objects(email_address=email).first()


def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user or not verify_password(password, user.password):
        return False
    return user
