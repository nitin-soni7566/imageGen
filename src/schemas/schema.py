from pydantic import EmailStr, SecretStr, BaseModel
from fastapi import Form, Query, Path, Body


class CreateUser:
    def __init__(
        self,
        username: EmailStr = Form(..., description="Valid Email Id"),
        password: str = Form(..., description="Password"),
        first_name: str = Form(..., description="User first name"),
        last_name: str = Form(..., description="User first name"),
    ):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name


class Login:
    def __init__(
        self,
        username: EmailStr = Form(..., description="Valid Email Id"),
        password: str = Form(..., description="Password"),
    ):
        self.username = username
        self.password = password
