from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from src.utilities.utils import *
from fastapi import UploadFile
from src.controller.image_services import genrate_image_var
from src.database.connect import get_db
from sqlalchemy.orm import Session


image_router = APIRouter()


@image_router.post("/file")
async def imagen(
    file: UploadFile,
    user: Annotated[dict, Depends(verify_user)],
    db: Session = Depends(get_db),
) -> JSONResponse:
    """This api will take image and return 4 varity of images

    Args:
        file (UploadFile): file

    Returns:
        JSONResponse:
    """
    return genrate_image_var(file, user, db)
