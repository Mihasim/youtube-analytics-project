import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video):
        self.id_video = id_video

        video_response = self.youtube.videos().list(part='snippet,statistics,'
                                                         'contentDetails,topicDetails',
                                                    id=id_video
                                                    ).execute()

        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.video_link: str = f"https://youtu.be/{id_video}"
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video):
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video, id_play_list):
        super().__init__(id_video)
        self.id_play_list = id_play_list

    def __str__(self):
        return f"{self.video_title}"
