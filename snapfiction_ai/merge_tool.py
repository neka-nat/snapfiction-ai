import os
import tempfile
import uuid

from moviepy.editor import VideoFileClip, concatenate_videoclips
from google.adk.tools.tool_context import ToolContext


async def merge_videos(video_ids: list[str], tool_context: ToolContext) -> str:
    """
    Merge videos into a single video.

    Args:
        video_ids: The IDs of the videos to merge.

    Returns:
        The path of the merged video.
    """
    tempfile_paths = []
    for video_id in video_ids:
        video_artifact = await tool_context.load_artifact(filename=video_id)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(video_artifact.inline_data.data)
            tempfile_paths.append(temp_file.name)
    output_path = f"generated_video_{uuid.uuid4()}.mp4"

    videos = [VideoFileClip(path) for path in tempfile_paths]
    final_video = concatenate_videoclips(videos)
    final_video.write_videofile(output_path)
    for tempfile_path in tempfile_paths:
        os.remove(tempfile_path)
    return os.path.abspath(output_path)
