from fastapi import FastAPI, Depends, status, APIRouter
from fastapi.responses import JSONResponse
from typing import Annotated
from src.database.connect import get_db, engine
from sqlalchemy.orm import Session
from src.schemas import schema
from src.schemas import models
from src.utilities.utils import *
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, File, UploadFile
from src.controller.authentication_services import create_user, user_login


auth_router = APIRouter(tags=["auth"])


@auth_router.post("/user")
def add_user(
    user_data: schema.CreateUser = Depends(), db: Session = Depends(get_db)
) -> JSONResponse:
    """This route is for create user in db

    Args:
        user_data (schema.CreateUser, optional): take user email password first name and last name to create user
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        JSONResponse: success response if user created successfully
    """
    return create_user(user_data, db)


@auth_router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> JSONResponse:
    """This is login api to authenticate user
    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends): take username and password
    Returns:
        JSONResponse: return token and token type

    """
    return user_login(form_data, db)
