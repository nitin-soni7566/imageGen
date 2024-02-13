from fastapi import FastAPI
from src.database.connect import engine
from src.schemas import models
from src.view import auth, imagen

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.auth_router)
app.include_router(imagen.image_router)
