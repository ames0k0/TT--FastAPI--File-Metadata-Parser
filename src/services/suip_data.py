import requests
from bs4 import BeautifulSoup

from core import exceptions
from .base import BaseService


class SuipDataService(BaseService):
    """SuipData Service"""

    SUIP_HOST: str = "https://suip.biz/ru/?act=mat"

    def parse_file_metadata(self, file_bytes) -> dict:
        """Uploades the given file to the 3-rd party service

        Returns
        -------
        dict - Parsed response

        Raises
        ------
        exceptions.ServiceIsUnavailable
        exceptions.ContentIsMissing
        exceptions.MetadataIsMissing
        """
        try:
            response = requests.post(
                url=self.SUIP_HOST,
                files={
                    "fileforsending": file_bytes,
                },
            )
        except Exception:
            raise exceptions.ServiceIsUnavailable()

        if (not response) or (response.status_code != 200):
            raise exceptions.ServiceIsUnavailable()

        soup = BeautifulSoup(response.text, "html.parser")

        news_container = soup.find(name="div", class_="news")
        if news_container is None:
            raise exceptions.ContentIsMissing("div.news")

        code_container = news_container.find("pre")  # type: ignore
        if code_container is None:
            raise exceptions.ContentIsMissing("div.news.pre")

        data = {}

        for line in code_container.text.split("\n"):  # type: ignore
            line_kv = line.split(":", maxsplit=1)
            if len(line_kv) != 2:
                continue

            key, value = (item.strip() for item in line_kv)
            if not all((key, value)):
                continue

            data[key] = value

        if not data:
            raise exceptions.MetadataIsMissing()

        return data
