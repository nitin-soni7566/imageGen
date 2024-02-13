import boto3
from src.core.config import settings

from botocore.client import Config

s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name="us-east-1",
    config=Config(max_pool_connections=500),
)
