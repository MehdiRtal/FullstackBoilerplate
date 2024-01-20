from pydantic import PostgresDsn, RedisDsn, HttpUrl
from pydantic_settings import BaseSettings
import os

from constants import Environment


class Settings(BaseSettings):
    ENVIRONEMENT: Environment | None = None

    DB_URL: PostgresDsn

    REDIS_URL: RedisDsn

    RQ_URL: RedisDsn

    CACHE_URL: RedisDsn

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    VERIFY_TOKEN_EXPIRE_MINUTES: int

    JWT_SECRET: str
    JWT_ALGORITHM: str

    SIGNATURE_SECRET: str

    SELLIX_API_KEY: str
    SELLIX_SIGNATURE_SECRET: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    SENDGRID_API_KEY: str

    TURNSTILE_SECRET_KEY: str
    TURNSTILE_SITE_KEY: str

    SENTRY_DSN: HttpUrl | None = None

environement = Environment(os.getenv("ENVIRONEMENT", Environment.DEV))
if environement.is_dev:
    settings = Settings(
        _env_file=(
            os.path.join(os.path.dirname(__file__), "base.env"),
            os.path.join(os.path.dirname(__file__), "dev.env")
        )
    )
elif environement.is_prod:
    settings = Settings(
        _env_file=(
            os.path.join(os.path.dirname(__file__), "base.env"),
            os.path.join(os.path.dirname(__file__), "prod.env")
        )
    )
settings.ENVIRONEMENT = environement
