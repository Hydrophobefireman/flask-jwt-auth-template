from magic import from_buffer

from app.exceptions import AppException
from app.settings import S3Settings

from .compress import optimize
from .config import build_s3_client, build_s3_client_for_presigned_url


def check_mimetype(b: bytes):
    ct = from_buffer(b[:4096], mime=True)
    if ct.split("/")[0] not in {"image", "video"}:
        raise AppException("Unsupported media type")
    return ct


def upload_media(media: bytes, path: str):
    s3_settings = S3Settings()
    ## Why not presigned post urls
    s3_client = build_s3_client(s3_settings)
    mt = check_mimetype(media)
    if mt.split("/")[0] == "image":
        media = optimize(media)
    # print(f"uploading {media[:100]} to {path}")
    s3_client.put_object(
        Bucket=s3_settings.bucket_name, Key=path, Body=media, ContentType=mt
    )

    return [path, mt]


def presign_url(path: str):
    s3_settings = S3Settings()
    s3_client_for_presigned = build_s3_client_for_presigned_url(s3_settings)
    if path.startswith("http:") or path.startswith("https:"):
        return {"path": "Deprecated", "url": path}
    url = s3_client_for_presigned.generate_presigned_url(
        "get_object",
        Params={"Bucket": s3_settings.bucket_name, "Key": path},
        ExpiresIn=43200,
    )
    return {"path": path, "url": url}
