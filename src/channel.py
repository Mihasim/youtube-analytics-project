import json
import os

from googleapiclient.discovery import build


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        self.__channel_id = channel_id
        channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.view_count = channel["items"][0]["statistics"]["viewCount"]

        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

    def __str__(self):
        return f"{self.title} ({self.url})"


    @property
    def channel_id(self):
        return self.__channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_id = self.__channel_id  # HighLoad Channel
        channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        printj(channel)

    @classmethod
    def get_service(cls):
        """
        возвращающий объект для работы с YouTube API
        """
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file):
        """
        сохраняющий в файл значения атрибутов экземпляра Channel
        """
        self.file = file
        attrib_dict = {"channel_id": self.__channel_id,
                       "title": self.title,
                       "description": self.description,
                       "url": self.url,
                       "subscriber_count": self.subscriber_count,
                       "video_count": self.video_count,
                       "view_count": self.view_count,
                       }
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(attrib_dict, f, indent=2, ensure_ascii=False)

    def __repr__(self):
        return f"{self.__class__.__name__},\n{self.__channel_id},\n{self.title},\n" \
               f"{self.description}, \n{self.url}, \n{self.subscriber_count}, \n" \
               f"{self.video_count}, \n{self.view_count}"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)
