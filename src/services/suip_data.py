import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException, status


class ServiceIsUnavailable(HTTPException):
    """SUIP Service is Unavailable"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ParserError: SUIP Service is Unavailable",
        )


class ContentIsMissing(HTTPException):
    """Could not parse the result from metadata server"""

    def __init__(self, missing_to_find: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"ParserError: Content for `{missing_to_find}` is missing!",
        )


class MetadataIsMissing(HTTPException):
    """Could not parse the result from metadata server"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="ParserError: No metadata found!",
        )


class SuipDataService:
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
            raise ServiceIsUnavailable()

        if (not response) or (response.status_code != 200):
            raise ServiceIsUnavailable()

        soup = BeautifulSoup(response.text, "html.parser")

        news_container = soup.find(name="div", class_="news")
        if news_container is None:
            raise ContentIsMissing("div.news")

        code_container = news_container.find("pre")  # type: ignore
        if code_container is None:
            raise ContentIsMissing("div.news.pre")

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
            raise MetadataIsMissing()

        return data
