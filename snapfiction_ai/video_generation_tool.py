import os
import time
import tempfile

from google import genai
from google.genai.types import GenerateVideosConfig, Image
from loguru import logger

from .utils.movie_utils import extract_last_frame
from .utils.storage import download_video, upload_image

_model_name = "veo-2.0-generate-001"


async def generate_video(
    prompt: str,
    image_uri: str,
    aspect_ratio: str = "16:9",
) -> dict[str, str]:
    """
    Generate a video from a prompt and image.
    8 seconds video is generated.

    Args:
        prompt: The prompt to generate the video from.
        image_uri: The URI of the image to generate the video from.
        aspect_ratio: The aspect ratio of the video.

    Returns:
        The URI of the generated video.
    """

    video_output_uri = f"gs://{os.environ['GOOGLE_STORAGE_BUCKET_NAME']}/videos"

    client = genai.Client()
    operation = client.models.generate_videos(
        model=_model_name,
        prompt=prompt,
        image=Image(gcs_uri=image_uri, mime_type="image/png"),
        config=GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            output_gcs_uri=video_output_uri,
        ),
    )

    while not operation.done:
        time.sleep(15)
        operation = client.operations.get(operation)
        logger.info(operation)

    if operation.response:
        video_uri = operation.result.generated_videos[0].video.uri
        video_bytes = download_video(video_uri)
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(video_bytes)
            temp_file_path = temp_file.name
            last_frame = extract_last_frame(temp_file_path)
        target_blob_name = os.path.dirname(video_uri) + "/last_frame.png"
        image_uri = upload_image(last_frame, target_blob_name)
        return {
            "status": "success",
            "video_uri": video_uri,
            "last_frame_uri": image_uri,
        }
    else:
        return {
            "status": "error",
            "error": "Failed to generate video",
        }
