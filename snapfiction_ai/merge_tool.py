import os
import tempfile
import io
import uuid

from moviepy.editor import AudioFileClip, CompositeAudioClip, VideoFileClip, concatenate_videoclips
from google.adk.tools.tool_context import ToolContext


async def merge_videos(video_ids: list[str], music_id: str, tool_context: ToolContext) -> dict[str, str]:
    """
    Merge videos into a single video.

    Args:
        video_ids: The IDs of the videos to merge.
        music_id: The ID of the music to merge.

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

    music_artifact = await tool_context.load_artifact(filename=music_id)
    music_clip = AudioFileClip(io.BytesIO(music_artifact.inline_data.data))

    if final_video.audio is None:
        final_audio = music_clip
    else:
        final_audio = CompositeAudioClip([final_video.audio, music_clip])
    final_video = final_video.set_audio(final_audio)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    for tempfile_path in tempfile_paths:
        os.remove(tempfile_path)
    return {
        "status": "success",
        "save_path": os.path.abspath(output_path),
    }
