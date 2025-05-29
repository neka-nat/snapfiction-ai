import os
import tempfile
import io
import uuid

from google.genai import types
from google.adk.tools.tool_context import ToolContext
from moviepy.editor import AudioFileClip, CompositeAudioClip, VideoFileClip, concatenate_videoclips


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
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(video_artifact.inline_data.data)
            tempfile_paths.append(temp_file.name)
    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

    videos = [VideoFileClip(path) for path in tempfile_paths]
    final_video = concatenate_videoclips(videos)

    music_artifact = await tool_context.load_artifact(filename=music_id)
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_file:
        temp_file.write(music_artifact.inline_data.data)
        music_clip = AudioFileClip(temp_file.name)

    if final_video.audio is None:
        final_audio = music_clip
    else:
        final_audio = CompositeAudioClip([final_video.audio, music_clip])
    final_audio = final_audio.subclip(0, final_video.duration)
    final_video = final_video.set_audio(final_audio)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    for tempfile_path in tempfile_paths:
        os.remove(tempfile_path)
    generated_video_id = f"generated_video_{uuid.uuid4()}.mp4"
    try:
        await tool_context.save_artifact(
            filename=generated_video_id,
            artifact=types.Part(
                inline_data=types.Blob(data=open(output_path, "rb").read(), mime_type="video/mp4"),
            ),
        )
        return {
            "status": "success",
            "generated_video_id": generated_video_id,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }
    finally:
        os.remove(output_path)
