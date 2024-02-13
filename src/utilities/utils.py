from passlib.hash import sha256_crypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def hash_password(password: str):
    hashed = sha256_crypt.using(rounds=5000).hash(password)
    return hashed


def verify_password(password, hashed):

    return sha256_crypt.verify(password, hashed)


def create_token(user_email: str, user_id: int):
    encode = {"sub": user_email, "id": user_id}
    expire = datetime.utcnow() + timedelta(minutes=20)
    encode.update({"exp": expire})
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def verify_user(token: Annotated[str, Depends(oauth2_scheme)]):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username = payload["sub"]
        user_id = payload["id"]

        return {"email": username, "id": user_id}
    except JWTError as e:

        return {"exception": e}
