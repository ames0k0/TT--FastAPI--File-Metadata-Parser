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
