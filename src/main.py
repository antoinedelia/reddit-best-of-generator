import argparse
import os
from warnings import resetwarnings
from reddit import Reddit
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

parser = argparse.ArgumentParser(description="Reddit Best Of Generator")


def main():
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

    args = parser.parse_args()

    subreddit = args.subreddit
    type = args.type
    time = args.time
    upload_to_youtube = args.upload_to_youtube
    nsfw = args.nsfw
    posts_limit = args.posts_limit

    # 1 - Get the posts from Reddit
    reddit = Reddit(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT)
    if type == "hot":
        posts = reddit.get_hot_posts(subreddit, posts_limit, nsfw)
        for post in posts:
            if f"https://www.reddit.com{post.permalink}" == post.url:
                logger.info(f"Post {post.title} is not a media")
            else:
                logger.info(f"This post with score {post.score} and title {post.title}: {post.url}. Selftext: {post.selftext}")
    elif type == "top":
        posts = reddit.get_top_posts(subreddit, time, posts_limit, nsfw)

    # 2 - Download the media from the posts
    # https://stackoverflow.com/questions/56950987/download-file-from-url-and-save-it-in-a-folder-python

    # 3 - Create the video by combining the media

    # 4 - Upload the media to Youtube


if __name__ == "__main__":
    main()
