import os
import uuid

from google.cloud import storage


def upload_image(image_bytes: bytes, target_blob_name: str | None = None) -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.environ["GOOGLE_STORAGE_BUCKET_NAME"])
    blob_name = target_blob_name or f"images/{uuid.uuid4()}.png"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(image_bytes)
    return f"gs://{os.environ['GOOGLE_STORAGE_BUCKET_NAME']}/{blob_name}"


def download_video(video_uri: str) -> bytes:
    bucket_name, blob_name = video_uri.replace("gs://", "").split("/", 1)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob.download_as_bytes()
