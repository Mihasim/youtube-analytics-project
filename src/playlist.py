import os
from googleapiclient.discovery import build
import isodate
from datetime import timedelta


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, pl_id):
        self.pl_id = pl_id
        self.url = f"https://www.youtube.com/playlist?list={self.pl_id}"
        playlist_videos = self.youtube.playlists().list(part="snippet",
                                                        id=self.pl_id).execute()
        self.title = playlist_videos['items'][0]['snippet']['title']

        playlist_videos = self.youtube.playlistItems().list(playlistId=pl_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(video_ids)
                                                         ).execute()

    @property
    def total_duration(self):
        """
        Получаем данные по видеороликам в плейлисте,
        Суммируем длительности видеороликов из плейлиста и возвращаем сумму
        """

        # Получаем суммарное время видеороликов
        all_time = timedelta(seconds=0)
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            all_time += duration
        return all_time

    def show_best_video(self):

        i = 0
        max_likes = 0
        for items in self.video_response:
            likes_video = int(self.video_response['items'][i]['statistics']['likeCount'])
            if max_likes < likes_video:
                url_best_video = self.video_response['items'][i]['id']
            i += 1
        return f"https://youtu.be/{url_best_video}"
