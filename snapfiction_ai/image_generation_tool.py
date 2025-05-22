import vertexai
from loguru import logger
from vertexai.preview.vision_models import ImageGenerationModel

from .utils.storage import upload_image


_model_name = "imagen-4.0-generate-preview-05-20"
# _model_name = "imagen-3.0-generate-002"


async def generate_image(prompt: str, aspect_ratio: str = "1:1") -> dict[str, str]:
    """
    Generate an image from a prompt.

    Args:
        prompt: The prompt to generate the image from.
        aspect_ratio: The aspect ratio of the image.

    Returns:
        The URI of the generated image.
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
        return {
            "status": "error",
            "error": "Failed to generate image",
        }

    logger.info(f"Created output image using {len(response.images[0]._image_bytes)} bytes")

    image_uri = upload_image(response.images[0]._image_bytes)

    return {
        "status": "success",
        "image_uri": image_uri,
    }
