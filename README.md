# Reddit Best Of Generator

Automatic generation of video with top posts from a subreddit.

## Getting Started

Downloading ImageMagick is required to run this program.

```sh
sudo apt-get install imagemagick
sudo apt-get install libraqm-dev

# Optional - some people had problems with the policy file, see: https://github.com/Zulko/moviepy/issues/401
sudo vim /etc/ImageMagick-7/policy.xml
```

To insert the posts's titles, we use the Roboto font. If you don't have it, please install it or update the font in the code.

### Youtube credentials

1. https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred

2. Place the `client_secrets.json` file at the root of the project.

## Run the script

```sh
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Reddit credentials, to create them, go to https://www.reddit.com/prefs/apps/
echo REDDIT_CLIENT_ID=YOUR_REDDIT_CLIENT_ID >> .env
echo REDDIT_CLIENT_SECRET=YOUR_REDDIT_CLIENT_SECRET >> .env
echo REDDIT_USER_AGENT=SOME_USER_AGENT >> .env

python src/main.py --subreddit=funny --output=output.mp4
python src/main.py --subreddit=TikTokCringe -output=output.mp4 --type=top --time=month --keep-temp-files --posts-limit=3
python src/main.py --subreddit=FortniteBr -output=output.mp4 --type=top --time=month  --keep-temp-files
```
