import pytube


class Youtube:
    def __init__(self, url):
        self.url = url
        self.yt = None

    def upload(self):
        self.yt = pytube.YouTube(self.url)
        self.yt.streams.first().download()
