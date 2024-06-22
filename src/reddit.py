import praw


class Reddit:
    def __init__(self, client_id, client_secret, user_agent, username: str = "", password: str = "", otp: int = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.username = username

        if username and password and otp:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent,
                username=username,
                password=f"{password}:{otp}",
            )
        else:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent,
            )

    def get_hot_posts(self, subreddit: str, limit: int = 10, include_nsfw: bool = False) -> list:
        """Get the last posts from a subreddit."""
        subreddit = self.reddit.subreddit(subreddit)
        posts = subreddit.hot(limit=limit)
        if not include_nsfw:
            posts = [post for post in posts if not post.over_18]

        return posts

    def get_new_posts(
        self, subreddit: str, limit: int = 10, include_nsfw: bool = False
    ) -> praw.models.listing.generator.ListingGenerator:
        """Get the last posts from a subreddit."""
        subreddit = self.reddit.subreddit(subreddit)
        print(subreddit.display_name)
        posts = subreddit.search(limit=limit)
        if not include_nsfw:
            posts = [post for post in posts if not post.over_18]

        return posts

    def get_top_posts(self, subreddit: str, time: str, limit: int = 10, include_nsfw: bool = False) -> list:
        """Get the last posts from a subreddit."""
        subreddit = self.reddit.subreddit(subreddit)
        posts = subreddit.top(time_filter=time, limit=limit)
        if not include_nsfw:
            posts = [post for post in posts if not post.over_18]

        return posts
