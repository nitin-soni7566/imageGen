from src.database.base import Base
from sqlalchemy import Integer, Column, String, DateTime
from datetime import datetime


class User(Base):

    __tablename__ = "usertable"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    # created_at = Column(DateTime, default=datetime.timestamp(datetime.utcnow()))


class ImageGen(Base):

    __tablename__ = "image_gen"
    img_id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String, unique=True, index=True)
    key = Column(String)
    filename = Column(String)
    upload_by = Column(String)
