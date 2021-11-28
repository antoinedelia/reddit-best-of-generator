# Reddit Best Of Generator

Automatic generation of video with top posts from a subreddit.

## Getting Started

Downloading ImageMagick is required to run this program.

```shell
$ sudo alien -i ImageMagick-7.1.0-16.x86_64.rpm
$ sudo alien -i ImageMagick-libs-7.1.0-16.x86_64.rpm
$ sudo apt-get install libraqm-dev

# Optional - some people had problems with the policy file, see: https://github.com/Zulko/moviepy/issues/401
$ sudo vim /etc/ImageMagick-7/policy.xml
```

```shell
$ pip install -r requirements.txt

# Reddit credentials, to create them, go to https://www.reddit.com/prefs/apps/
$ echo REDDIT_CLIENT_ID=YOUR_REDDIT_CLIENT_ID >> .env
$ echo REDDIT_CLIENT_SECRTET=YOUR_REDDIT_CLIENT_SECRET >> .env
$ echo REDDIT_USER_AGENT=SOME_USER_AGENT >> .env

$ python src/main.py --subreddit=funny --output=output.mp4
```
