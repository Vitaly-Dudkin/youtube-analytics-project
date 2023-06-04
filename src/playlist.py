import datetime
import os

import isodate
from src.utils import find_value
from googleapiclient.discovery import build


class PlayList:
    """
    Класс для плейлиста
    """
    service = "youtube"
    version = "v3"
    name_key = os.getenv("YT_API_KEY")
    manager = build(service, version, developerKey=name_key)

    def __init__(self, play_list_id):
        self.play_list_id = play_list_id
        self.title = None
        self.url = None
        self.__total_duration = None

        self.set_atr()

    def set_atr(self) -> None:
        """
        Устанавливает значения основных атрибутов объекта
        на основании полученных по id данных play_list_id
        """

        playlist = self.get_info()

        self.title = find_value(playlist, "title")
        self.url = f'https://www.youtube.com/playlist?list={self.play_list_id}'
        self.__total_duration = self.get_total_duration()

    def get_info(self) -> dict:
        """Получает данные о play_list по его id"""

        playlist_response = self.manager.playlists().list(id=self.play_list_id,
                                                          part='contentDetails, snippet').execute()
        return playlist_response

    def get_video_response(self) -> dict:
        """
        Получаем словарь с данными о play_list
        """
        playlist_videos = self.manager.playlistItems().list(playlistId=self.play_list_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        # printj(playlist_videos)
        #
        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        # print(video_ids)

        '''
        вывести длительности видеороликов из плейлиста
        docs: https://developers.google.com/youtube/v3/docs/videos/list
        '''
        video_response = self.manager.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        return video_response
        # printj(video_response)

    def get_total_duration(self) -> datetime:
        """
        Получаем сумму длительности видеороликов в play_list
        """
        video_response = self.get_video_response()
        lst = []
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            lst.append(duration)
        return sum(lst, datetime.timedelta())

    @property
    def total_duration(self):
        return self.__total_duration

    def show_best_video(self) -> str:
        """
        Получаем ссылку на самое популярное видео
        - из плейлиста (по количеству лайков)
        """
        dict_likes = {}
        video_response = self.get_video_response()
        for video in video_response['items']:
            likes = int(video['statistics']['likeCount'])
            url = video['id']
            dict_likes[likes] = url
        best_video_url = max(dict_likes.keys())
        return f'https://youtu.be/{dict_likes[best_video_url]}'






