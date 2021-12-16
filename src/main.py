import argparse
import os
import media_helper
from reddit import Reddit
from dotenv import load_dotenv
from loguru import logger
from typing import List

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

TEMP_FOLDER = "temp"
DESTINATION_FOLDER = "output"
DESTINATION_FILE_NAME = "output.mp4"

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]

parser = argparse.ArgumentParser(description="Reddit Best Of Generator")


def main():
    logger.add("logs/file_{time}.log")

    parser.add_argument("--subreddit", "-sub", required=True,
                        help="specify subreddit to get posts from",
                        dest="subreddit")

    parser.add_argument("--type", required=False,
                        help="specify the type of content to get (hot, new, top, rising, controversial, gilded)",
                        dest="type", default="hot")

    parser.add_argument("--time", required=False,
                        help="if type is top, specify the period of time (hour, day, week, month, year, all)",
                        dest="time", default="day")

    parser.add_argument("--upload-to-youtube", required=False, action="store_true",
                        help="whether to upload the output video to Youtube",
                        dest="upload_to_youtube")

    parser.add_argument("--nsfw", required=False, action="store_true",
                        help="whether to include nsfw content",
                        dest="nsfw", default=False)

    parser.add_argument("--posts-limit", "-limit", required=False, type=int,
                        help="specify how many posts to get to make the best of",
                        dest="posts_limit", default=10)

    parser.add_argument("--output-path", "-output", required=True, type=str,
                        help="specify the output of where to store the final result of your video",
                        dest="output_path")

    parser.add_argument("--keep-temp-files", required=False, action="store_true",
                        help="whether we should keep the temporary files downloaded, defaults to false",
                        dest="keep_temp_files")

    args = parser.parse_args()

    subreddit = args.subreddit
    type = args.type
    time = args.time
    upload_to_youtube = args.upload_to_youtube
    nsfw = args.nsfw
    posts_limit = args.posts_limit
    keep_temp_files = args.keep_temp_files

    logger.info(f"Getting {posts_limit} {type} posts from /r/{subreddit}")
    if type == "top":
        logger.info(f"Top posts will be filtered by {time}")
    logger.info(f"NSFW content will be {'included' if nsfw else 'excluded'}")

    # 1 - Get the posts from Reddit
    reddit = Reddit(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT)
    if type == "hot":
        posts = reddit.get_hot_posts(subreddit, posts_limit, nsfw)
    elif type == "top":
        posts = reddit.get_top_posts(subreddit, time, posts_limit, nsfw)

    logger.info(f"{len(posts)} posts found!")

    filtered_posts: List['media_helper.Media'] = []

    # We filter out posts that are self posts (not linking to a media such as image or video)
    for post in posts:
        if f"https://www.reddit.com{post.permalink}" == post.url or post.url.startswith("https://www.reddit.com"):
            logger.info(f"Post {post.id} is not a media, skipping it.")
            continue

        if post.__dict__["pinned"]:
            logger.info(f"Post {post.id} is a pinned post, skipping it.")
            continue

        if post.__dict__["stickied"]:
            logger.info(f"Post {post.id} is a stickied post, skipping it.")
            continue

        if post.__dict__["distinguished"] == "moderator":
            logger.info(f"Post {post.id} is a moderator post, skipping it.")
            continue

        _, file_extension = os.path.splitext(post.url)
        if file_extension in IMAGE_EXTENSIONS:
            logger.info(f"Post {post.id} is a image, skipping it.")
            continue

        if post.url.startswith("https://v.redd.it"):
            original_url = post.__dict__["secure_media"]["reddit_video"]["fallback_url"]
            new_media = media_helper.Media(
                id=post.id,
                title=post.title,
                type=post.__dict__["post_hint"],
                is_reddit_media=True,
                original_url=original_url,
                reddit_video_url=original_url.split("?")[0],
            )
            # Old v.redd.it links have a different audio url
            if "mp4" in original_url:
                new_media.reddit_audio_url = "/".join(original_url.split("?")[0].split("/")[:-1]) + "/DASH_audio.mp4"
            else:
                new_media.reddit_audio_url = "/".join(original_url.split("?")[0].split("/")[:-1]) + "/audio"

            filtered_posts.append(new_media)
        else:
            filtered_posts.append(
                media_helper.Media(
                    id=post.id,
                    title=post.title,
                    type=post.__dict__["post_hint"],
                    is_reddit_media=False,
                    original_url=post.url,
                )
            )

    logger.info(f"{len(filtered_posts)} media posts found!")

    # Unused for now but could be useful in the future
    # post.__dict__["post_hint"] -> "hosted:video"
    # post.__dict__["domain"] -> "v.redd.it"
    # post.__dict__["url_overridden_by_dest"] -> "https://v.redd.it/1xrjl5eo5k181"
    # post.__dict__["archived"] -> False
    # post.__dict__["spoiler"] -> False
    # post.__dict__["locked"] -> False
    # post.__dict__["is_video"] -> True
    # post.__dict__["media"]["reddit_video"]["duration"] -> 20
    # post.__dict__["media"]["reddit_video"]["is_gif"] -> False

    # 2 - Download the media from the posts
    for post in filtered_posts:
        if post.is_reddit_media:
            logger.info(f"Downloading Reddit video {post.reddit_video_url}")
            media_helper.download_from_url(f"video_{post.id}", post.reddit_video_url, TEMP_FOLDER)

            logger.info(f"Downloading Reddit audio {post.reddit_audio_url}")
            media_helper.download_from_url(f"audio_{post.id}", post.reddit_audio_url, TEMP_FOLDER)
        else:
            logger.info(f"Downloading video {post.original_url}")
            media_helper.download_from_url(f"video_{post.id}", post.original_url, TEMP_FOLDER)

    # 3 - Create the video by combining the media
    media_helper.combine_medias(filtered_posts, TEMP_FOLDER, DESTINATION_FOLDER, DESTINATION_FILE_NAME)

    # 4 - Upload the media to Youtube
    if upload_to_youtube:
        logger.info("Uploading to Youtube")

    # 5 - Clean up the temp folder
    if not keep_temp_files:
        media_helper.delete_folder(TEMP_FOLDER)


if __name__ == "__main__":
    main()
