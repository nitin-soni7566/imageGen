from PIL import Image
from datetime import datetime
from fastapi import UploadFile
from src.database.bucket import s3
from src.core.config import settings
import requests
import os
from src.schemas import models
from datetime import datetime
from sqlalchemy.orm import Session


def thumbnail_image(filename, email):
    new_file = "thum_" + filename
    key = f"file/{email}/{new_file}"
    img = Image.open(filename)
    thum = img.resize((200, 300))
    thum.save("thum_" + filename)
    update_file_into_s3(new_file, key)


def medium_image(filename, email):
    new_file = "mid_" + filename
    key = f"file/{email}/{new_file}"
    img = Image.open(filename)
    mid = img.resize((500, 500))
    mid.save("mid_" + filename)
    update_file_into_s3(new_file, key)


def large_image(filename, email):
    new_file = "large_" + filename
    key = f"file/{email}/{new_file}"
    img = Image.open(filename)
    larg = img.resize((1028, 786))
    larg.save(new_file)
    update_file_into_s3(new_file, key)


def gray_scale_image(filename, email):
    new_file = "gray_" + filename
    key = f"file/{email}/{new_file}"
    img = Image.open(filename)
    gray = img.convert("L")
    gray.save(new_file)
    update_file_into_s3(new_file, key)


def get_images_url(key: str, org: str):
    keys = ["", "gray_", "thum_", "large_", "mid_"]
    urls = {}
    try:
        for k in keys:
            url = s3.generate_presigned_url(
                ClientMethod="get_object",
                ExpiresIn=300,
                Params={
                    "Bucket": settings.AWS_S3_BUCKET,
                    "Key": f"{key.replace('.com/',f'.com/{k}')}",
                    "ResponseContentDisposition": f"attachment;filename={k}{org}",
                },
            )
            if k == "":
                urls["org"] = url
            else:
                urls[k] = url

        return urls
    except Exception as e:

        print(e)


def update_file_into_s3(filename: str, key: str):
    try:
        response = s3.generate_presigned_post(
            settings.AWS_S3_BUCKET,
            key,
            Fields=None,
            Conditions=None,
            ExpiresIn=3600,
        )
        with open(filename, "rb") as f:
            files = {"file": (filename, f)}
            http_response = requests.post(
                response["url"], data=response["fields"], files=files
            )
        if os.path.exists(filename):
            os.remove(filename)
            print("deleted -->")
        print(http_response)
        return http_response.text
    except Exception as e:

        print(e)
        return e


def genrate_image_var(file: UploadFile, user: dict, db: Session):

    filename = f"{datetime.timestamp(datetime.utcnow())}_{file.filename}"
    email = user["email"]
    key = f"file/{user['email']}/{filename}"
    data = file.file.read()
    with open(filename, "wb") as f:
        f.write(data)
    file.file.close()
    try:
        new_entry = models.ImageGen(
            key=key,
            timestamp=datetime.timestamp(datetime.utcnow()),
            filename=file.filename,
            upload_by=email,
        )
        db.add(new_entry)
        db.commit()
    except Exception as e:
        print(e)
    thumbnail_image(filename, email)
    large_image(filename, email)
    medium_image(filename, email)
    gray_scale_image(filename, email)
    update_file_into_s3(filename, key)
    data = get_images_url(key, file.filename)

    return {"urls": data}
