import uuid

import vertexai
from google.genai import types
from google.adk.tools.tool_context import ToolContext
from loguru import logger
from vertexai.preview.vision_models import ImageGenerationModel


_model_name = "imagen-4.0-generate-preview-05-20"
# _model_name = "imagen-3.0-generate-002"


async def generate_image(prompt: str, aspect_ratio: str, tool_context: ToolContext) -> dict[str, str]:
    """
    Generate an image from a prompt.

    Args:
        prompt: The prompt to generate the image from.
        aspect_ratio: The aspect ratio of the image (e.g. "1:1", "16:9", "9:16").

    Returns:
        The ID of the generated image.
    """

    vertexai.init()

    model = ImageGenerationModel.from_pretrained(_model_name)

    response = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        language="en",
        aspect_ratio=aspect_ratio,
        safety_filter_level="block_only_high",
        person_generation="allow_adult",
    )

    if not response.images:
        logger.error(f"Failed to generate image: {response}")
        return {
            "status": "error",
            "error": "Failed to generate image",
        }

    logger.info(f"Created output image using {len(response.images[0]._image_bytes)} bytes")

    image_id = f"image_{uuid.uuid4()}.png"
    await tool_context.save_artifact(
        filename=image_id,
        artifact=types.Part(
            inline_data=types.Blob(
                data=response.images[0]._image_bytes,
                mime_type="image/png",
            ),
        ),
    )
    logger.info(f"Added image artifact: {image_id}")

    return {
        "status": "success",
        "image_id": image_id,
    }
