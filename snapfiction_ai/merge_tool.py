import os
import tempfile
import uuid

from moviepy.editor import VideoFileClip, concatenate_videoclips

from .utils.storage import download_video


async def merge_videos(video_uris: list[str]) -> str:
    """
    Merge videos into a single video.

    Args:
        video_uris: The URIs of the videos to merge.

    Returns:
        The path of the merged video.
    """
    tempfile_paths = []
    for video_uri in video_uris:
        video_bytes = download_video(video_uri)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(video_bytes)
            tempfile_paths.append(temp_file.name)
    output_path = f"generated_video_{uuid.uuid4()}.mp4"

    videos = [VideoFileClip(path) for path in tempfile_paths]
    final_video = concatenate_videoclips(videos)
    final_video.write_videofile(output_path)
    for tempfile_path in tempfile_paths:
        os.remove(tempfile_path)
    return output_path
