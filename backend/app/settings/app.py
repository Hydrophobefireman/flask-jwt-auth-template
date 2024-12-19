from pydantic_settings import BaseSettings
from pydantic import AfterValidator, PostgresDsn, Field
from typing import Annotated, Optional
from pathlib import Path
from os import path, environ
from dotenv import load_dotenv

load_dotenv()


class _AppSettings(BaseSettings):
    token_expiration_time: Annotated[int, AfterValidator(lambda x: x * 60)]
    jwt_signing_key: str
    flask_secret: str
    database_url: Annotated[
        PostgresDsn,
        AfterValidator(
            lambda x: PostgresDsn(
                str(x)
                .replace("postgres://", "postgresql://")
                .replace("postgresql://", "postgresql+psycopg://")
            )
        ),
    ]
    refresh_token_salt: str
    disable_caching: Optional[bool] = Field(default=False)
    static_dir: Optional[str] = str(
        Path(path.dirname(path.realpath(__file__)), "..", "static").resolve()
    )
    is_prod: bool
    email_features_enabled: Optional[bool] = Field(default=False)


app_settings = _AppSettings(is_prod=environ.get("IS_DEV") is None)
