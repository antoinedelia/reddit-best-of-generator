import os
import shutil
import requests
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import moviepy.editor as editor
from loguru import logger

VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov"]

PROVIDER_EXTENSIONS_MAP = {
    "youtube": ".mp4",
    "youtu.be": ".mp4",
    "imgur": ".gif",
    "reddit": ".jpg",
    "gfycat": ".gif",
}


def download_from_url(id: str, url: str, dest_folder: str):
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
        return

    # TODO Need youtube-dl to download the video
    if "youtube" in url or "youtu.be" in url:
        logger.warning(f"{url} is a youtube video, not implemented yet.")
        return

    if "imgur" in url:
        logger.warning(f"{url} is an imgur link, not implemented yet.")
        return

    # Gfycat redirects to a web page, not directly to the video
    if "gfycat" in url:
        logger.warning(f"{url} is an gfycat link, not implemented yet.")
        return

    r = requests.get(url, stream=True)
    if r.ok:
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:
        logger.warning("Download failed: status code {}\n{}".format(r.status_code, r.text))


def combine_medias(posts: list, source_folder: str, dest_folder: str, dest_filename: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    filenames = next(os.walk(source_folder), (None, None, []))[2]
    clips = []
    for file in filenames:
        file_path = os.path.join(source_folder, file)
        post = next(iter(filter(lambda p: file.startswith(p.id), posts)), None)

        _, file_extension = os.path.splitext(file)

        if file_extension in VIDEO_EXTENSIONS:
            logger.info(f"Adding {file_path} to the video")
            video = VideoFileClip(file_path)

            # Make the text. Many more options are available.
            txt_clip = TextClip(post.title, font="DejaVu-Sans-Mono", fontsize=20, color='white')
            txt_clip = txt_clip.set_duration(video.duration)
            txt_clip = txt_clip.set_position("center")

            result = CompositeVideoClip([video, txt_clip])  # Overlay text on video
            clips.append(result)

    final_path = os.path.join(dest_folder, dest_filename)
    logger.info(f"Combining {len(clips)} videos in {final_path}")
    concat_clip = editor.concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(final_path, codec="mpeg4")


def delete_folder(folder_path: str):
    shutil.rmtree(folder_path)
