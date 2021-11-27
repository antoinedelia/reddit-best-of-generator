# Reddit Best Of Generator

Automatic generation of video with top posts from a subreddit.

## Getting Started

```shell
$ pip install -r requirements.txt

$ echo REDDIT_CLIENT_ID=YOUR_REDDIT_CLIENT_ID >> .env
$ echo REDDIT_CLIENT_SECRTET=YOUR_REDDIT_CLIENT_SECRET >> .env
$ echo REDDIT_USER_AGENT=SOME_USER_AGENT >> .env

$ python src/main.py --subreddit=funny --output=output.mp4
```
