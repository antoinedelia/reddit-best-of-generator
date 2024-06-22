import os
import shutil
import textwrap
from dataclasses import dataclass
from typing import List

import moviepy.editor as editor
import requests
from loguru import logger
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import ColorClip, TextClip

VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov"]

PROVIDER_EXTENSIONS_MAP = {
    "youtube": ".mp4",
    "youtu.be": ".mp4",
    "imgur": ".gif",
    "reddit": ".jpg",
    "gfycat": ".gif",
    "redgifs": ".mp4",
    "v.redd.it": ".mp4",
}


@dataclass
class Media:
    id: str
    title: str
    type: str
    original_url: str
    is_reddit_media: bool = False
    reddit_video_url: str = None
    reddit_audio_url: str = None


def download_from_url(id: str, url: str, dest_folder: str) -> bool:
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    _, file_extension = os.path.splitext(url)
    if not file_extension:
        for provider, extension in PROVIDER_EXTENSIONS_MAP.items():
            if provider in url:
                file_extension = extension
                break

    filename = id + file_extension
    file_path = os.path.join(dest_folder, filename)

    if os.path.isfile(file_path):
        logger.info(f"{file_path} already exists.")
        return False

    # TODO Need youtube-dl to download the video
    if "youtube" in url or "youtu.be" in url:
        logger.warning(f"{url} is a youtube video, not implemented yet.")
        return False

    if "imgur" in url:
        logger.warning(f"{url} is an imgur link, not implemented yet.")
        return False

    # Gfycat redirects to a web page, not directly to the video
    if "gfycat" in url:
        logger.warning(f"{url} is a gfycat link, not implemented yet.")
        return False

    if "redgifs" in url:
        logger.warning(f"{url} is a gfycat link, not implemented yet.")
        return False

    if "twitch" in url:
        logger.warning(f"{url} is a twitch link, not implemented yet.")
        return False

    r = requests.get(url, stream=True, timeout=10)
    if r.ok:
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:
        logger.warning("Download failed: status code {}\n{}".format(r.status_code, r.text))
        return False
    return True


def combine_medias(posts: List[Media], source_folder: str, dest_folder: str, dest_filename: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    clips = []
    logger.info(posts)
    for post in posts:
        if post.is_reddit_media:
            video_file_path = os.path.join(source_folder, f"video_{post.id}.mp4")
            audio_file_path = os.path.join(source_folder, f"audio_{post.id}.mp4")

            logger.info(f"Combinining audio and video of post {post.id}")
            video = editor.VideoFileClip(video_file_path)
            video = video.resize(width=1920) if video.w >= video.h else video.resize(height=1080)

            if video.w > 1920:
                video = video.resize(width=1920)
            if video.h > 1080:
                video = video.resize(height=1080)

            try:
                audio = editor.AudioFileClip(audio_file_path)
                video = video.set_audio(audio)
            except Exception as e:
                logger.warning(f"Could not load audio for post {post.id}: {e}")

            # Reduce the number of chars per line, depending on video width
            max_chars = 150 if video.w > 1500 else 75 if video.w > 1000 else 40
            text_clip = TextClip(
                "\n".join(textwrap.wrap(post.title, max_chars, break_long_words=False)),
                font="Roboto-Black",
                fontsize=25,
                color="white",
            )
            text_clip = text_clip.set_position("center")
            image_width, image_height = text_clip.size
            padding = 20
            color_clip = ColorClip(size=(image_width + padding, image_height + padding), color=(0, 0, 0))
            color_clip = color_clip.set_opacity(0.8)

            final_text_clip = CompositeVideoClip([color_clip, text_clip])
            final_text_clip = final_text_clip.set_duration(video.duration)
            final_text_clip = final_text_clip.set_position(("left", "bottom"))

            result = CompositeVideoClip([video, final_text_clip])  # Overlay text on video
            clips.append(result)

    final_path = os.path.join(dest_folder, dest_filename)
    logger.info(f"Combining {len(clips)} videos in {final_path}")
    concat_clip = editor.concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(final_path)


def delete_folder(folder_path: str):
    shutil.rmtree(folder_path)
