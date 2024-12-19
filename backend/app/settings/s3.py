from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl
from dotenv import load_dotenv

load_dotenv()


class S3Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="s3_")
    endpoint_url: HttpUrl
    access_key_id: str
    secret_access_key: str
    bucket_name: str


