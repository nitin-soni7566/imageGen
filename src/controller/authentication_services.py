from src.schemas import schema
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from src.schemas import models
from src.utilities.utils import hash_password, verify_password, create_token
from fastapi import status


def create_user(user_data: schema.CreateUser, db: Session):

    user = db.query(models.User).filter(models.User.email == user_data.username).first()
    if user is None:
        new_user = models.User(
            email=user_data.username,
            password=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        db.add(new_user)
        db.commit()
        return JSONResponse(
            content={"msg": "User created succssfully"},
            status_code=status.HTTP_201_CREATED,
        )

    return JSONResponse(
        content={"msg": "User allready exsit"},
        status_code=status.HTTP_409_CONFLICT,
    )


def user_login(user_data, db: Session):

    user = db.query(models.User).filter(models.User.email == user_data.username).first()
    print(user)
    if not user:
        return JSONResponse(
            content={"msg": "Invalid username password"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if verify_password(user_data.password, user.password):

        token = create_token(user.email, user.id)
        return JSONResponse(
            content={"access_token": token, "token_type": "bearer"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"msg": "Invalid username password"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
