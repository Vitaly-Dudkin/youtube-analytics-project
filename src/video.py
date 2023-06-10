from src.channel import Channel
from src.utils import find_value


class Video(Channel):
    def __init__(self, video_id):

        self.__video_id = video_id

        try:
            self.set_atr()

        except IndexError:

            self.__title = None
            self.__url = None
            self.__views_count = None
            self.__like_count = None

    @property
    def video_id(self):
        return self.__video_id

    @video_id.setter
    def video_id(self, video_id):
        self.__video_id = video_id
        self.set_atr()

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def views_count(self):
        return self.__views_count

    @views_count.setter
    def views_count(self, views_count):
        self.__views_count = views_count

    @property
    def like_count(self):
        return self.__likes_count

    @like_count.setter
    def like_count(self, likes_count):
        self.__like_count = likes_count

    def get_info(self) -> dict:
        """Получает данные о канале по его id"""

        video = self.get_service()

        video_response = video.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                             id=self.__video_id
                                             ).execute()
        return video_response

    def set_atr(self) -> None:
        """
        Устанавливает значения основных атрибутов объекта
        на основании полученных по id данных канала
        """

        channel = self.get_info()

        self.__title = find_value(channel, "title")
        self.__url = f'https://www.youtube.com/channel/{find_value(channel, "id")}'
        self.__likes_count = find_value(channel, "videoCount")
        self.__views_count = find_value(channel, "viewCount")

    def __str__(self):
        return f'{self.__title}'


class PLVideo(Video):
    def __init__(self, video_id, video_pl):
        super().__init__(video_id)
        self.video_pl = video_pl

