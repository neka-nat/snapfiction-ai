import base64
import io
import os
import uuid

from google.adk.tools import ToolContext
from google.cloud import aiplatform
from google.genai import types
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from loguru import logger
from pydub import AudioSegment


async def generate_music(prompt: str, tool_context: ToolContext) -> dict[str, str]:
    """
    Generate music from a prompt.

    Args:
        prompt: The prompt to generate the music from.

    Returns:
        The ID of the generated music.
    """

    try:
        client_options = {"api_endpoint": "aiplatform.googleapis.com"}
        client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

        params: dict[str, str|int] = {"prompt": prompt}
        instance = json_format.ParseDict(params, Value())
        instances = [instance]
        parameters = json_format.ParseDict({}, Value())

        endpoint_path = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/{os.environ['GOOGLE_CLOUD_LOCATION']}/publishers/google/models/lyria-002"
        logger.info(f"endpoint path {endpoint_path}")

        response = client.predict(endpoint=endpoint_path, instances=instances, parameters=parameters)
        predictions = response.predictions
        logger.info(f"Returned {len(predictions)} samples")

        bytes_b64 = dict(predictions[0])["bytesBase64Encoded"]
        decoded_audio_data = base64.b64decode(bytes_b64)
        audio_segment = AudioSegment.from_wav(io.BytesIO(decoded_audio_data))

        mp3_bytes = io.BytesIO()
        audio_segment.export(mp3_bytes, format="mp3")
        mp3_bytes.seek(0)
        music_id = f"music_{uuid.uuid4()}.mp3"
        await tool_context.save_artifact(
            filename=music_id,
            artifact=types.Part.from_bytes(
                data=mp3_bytes.getvalue(),
                mime_type="audio/mp3"
            ),
        )

        return {
            "status": "success",
            "music_id": music_id,
        }
    except Exception as e:
        logger.exception(f"failed to create the music. {e}")
        return {
            "status": "error",
            "error": str(e),
        }