from typing import List
from src.media_helper import Media, download_from_url, combine_medias

TEMP_FOLDER = "temp"


def test_combine_medias():
    posts: List[Media] = []
    posts.append(
        Media(
            id='r2m6y2',
            title='The female gaze',
            type='hosted:video',
            original_url='https://v.redd.it/c5p4xz3fpx181/DASH_720.mp4?source=fallback',
            is_reddit_media=True,
            reddit_video_url='https://v.redd.it/c5p4xz3fpx181/DASH_720.mp4',
            reddit_audio_url='https://v.redd.it/c5p4xz3fpx181/DASH_audio.mp4'
        )
    )

    posts.append(
        Media(
            id='r1740v',
            title='Welcome to the beginning of The End. Chapter 2 Finale I 12.4.21 I 4 PM ET',
            type='hosted:video',
            original_url='https://v.redd.it/1xrjl5eo5k181/DASH_720.mp4?source=fallback',
            is_reddit_media=True,
            reddit_video_url='https://v.redd.it/1xrjl5eo5k181/DASH_720.mp4',
            reddit_audio_url='https://v.redd.it/1xrjl5eo5k181/DASH_audio.mp4'
        )
    )
    for post in posts:
        if post.is_reddit_media:
            download_from_url(f"video_{post.id}", post.reddit_video_url, TEMP_FOLDER)
            download_from_url(f"audio_{post.id}", post.reddit_audio_url, TEMP_FOLDER)
        else:
            download_from_url(f"video_{post.id}", post.original_url, TEMP_FOLDER)

    combine_medias(posts, TEMP_FOLDER, "output/test", "test_output.mp4")


def test_small_video_large_title():
    posts: List[Media] = []
    posts.append(
        Media(
            id='23zhctljv3c11',
            title='This poor player is about to get banned cause he emoted. If four people were spectating me I’d be emoting too just to piss them off. There is absolutely 0 proof that this guy was stream sniping but we all know how Epic and Ninja suck each other off so this guy is getting banned for sure.',
            type='hosted:video',
            original_url='https://v.redd.it/23zhctljv3c11/DASH_4_8_M#mp4',
            is_reddit_media=True,
            reddit_video_url='https://v.redd.it/23zhctljv3c11/DASH_4_8_M',
            reddit_audio_url='https://v.redd.it/23zhctljv3c11/audio'
        )
    )
    for post in posts:
        if post.is_reddit_media:
            download_from_url(f"video_{post.id}", post.reddit_video_url, TEMP_FOLDER)
            download_from_url(f"audio_{post.id}", post.reddit_audio_url, TEMP_FOLDER)
        else:
            download_from_url(f"video_{post.id}", post.original_url, TEMP_FOLDER)

    combine_medias(posts, TEMP_FOLDER, "output/test", "test_output.mp4")
