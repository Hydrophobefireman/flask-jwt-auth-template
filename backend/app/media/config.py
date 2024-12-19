import boto3
from botocore.client import Config
from app.settings import s3_settings, app_settings

# Initialize the S3 client
s3_client = boto3.client(
    "s3",
    endpoint_url=str(s3_settings.endpoint_url),
    aws_access_key_id=s3_settings.access_key_id,  # MinIO access key
    aws_secret_access_key=s3_settings.secret_access_key,  # MinIO secret key
    config=Config(signature_version="s3v4"),
)


if not app_settings.is_prod:
    # otherwise we get a minio:9000 url that is useless locally
    s3_client_for_presigned_url = boto3.client(
        "s3",
        endpoint_url="http://localhost:9000",
        aws_access_key_id=s3_settings.access_key_id,  # MinIO access key
        aws_secret_access_key=s3_settings.secret_access_key,  # MinIO secret key
        config=Config(signature_version="s3v4"),
    )
else:
    s3_client_for_presigned_url = s3_client
