import boto3
from botocore.client import Config

from app.settings import S3Settings, app_settings


# Initialize the S3 client
def build_s3_client(s3_settings: S3Settings):
    return boto3.client(
        "s3",
        endpoint_url=str(s3_settings.endpoint_url),
        aws_access_key_id=s3_settings.access_key_id,
        aws_secret_access_key=s3_settings.secret_access_key,
        config=Config(signature_version="s3v4"),
    )


def build_s3_client_for_presigned_url(s3_settings: S3Settings):
    if not app_settings.is_prod and "minio" in s3_settings.endpoint_url.host:
        # otherwise we get a minio:9000 url that is useless locally
        return boto3.client(
            "s3",
            endpoint_url="http://localhost:9000",
            aws_access_key_id=s3_settings.access_key_id,
            aws_secret_access_key=s3_settings.secret_access_key,
            config=Config(signature_version="s3v4"),
        )
    return build_s3_client(s3_settings)
