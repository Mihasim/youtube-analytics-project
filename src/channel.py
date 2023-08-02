import json
import os

from googleapiclient.discovery import build


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Класс для ютуб-канала"""

    # api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey="AIzaSyBRoc9fFXoMqTxJ4vmacCAf-SHK90jfy0o")

    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_id = 'UCwHL6WHUarjGfUM_586me8w'  # HighLoad Channel
        channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        printj(channel)
