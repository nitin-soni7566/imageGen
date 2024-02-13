from pydantic_settings import BaseSettings, SettingsConfigDict
import warnings
import importlib.metadata

try:
    current_version = importlib.metadata.version("windvista-gateway-ms")
except Exception as e:
    current_version = "0.0.0"
warnings.filterwarnings("ignore", category=DeprecationWarning)


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DEFAULT_REGION: str
    AWS_S3_BUCKET: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


settings = Settings()
