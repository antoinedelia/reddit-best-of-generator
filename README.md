# Reddit Best Of Generator

Automatic generation of video with top posts from a subreddit.

## Getting Started

Downloading ImageMagick is required to run this program.

```sh
# Reference: https://gist.github.com/cuuupid/963db645047597723956af13ab87b73a
wget https://www.imagemagick.org/download/ImageMagick.tar.gz
tar xvzf ImageMagick.tar.gz
cd ImageMagick-*
./configure
make
sudo make install
sudo ldconfig /usr/local/lib
cd ..

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
# This is only required if your account has 2FA setup
# In that case, an OTP token will be asked when running the script
# Make sure to put your password into quotes to prevent issues with special characters
echo REDDIT_USERNAME=YOUR_REDDIT_USERNAME >> .env
echo REDDIT_USER_PASSWORD='YOUR_REDDIT_USER_PASSWORD' >> .env

python src/main.py --subreddit=funny --output=output.mp4
python src/main.py --subreddit=TikTokCringe -output=output.mp4 --type=top --time=month --keep-temp-files --posts-limit=3
python src/main.py --subreddit=FortniteBr -output=output.mp4 --type=top --time=month  --keep-temp-files
```
