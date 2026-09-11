class TaboolaError(BaseException):
    """
    Base error class for handling Taboola backstage API errors
    """

    def __init__(self, error, response):
        self.error = error
        self.response = response

    def __str__(self):
        return (
            f"{self.__class__.__name__} "
            f"[{self.response.status_code}]: {self.error}"
        )


class BadRequest(TaboolaError):
    """
    400 HTTP Errors
    """


class Unauthorized(TaboolaError):
    """
    401 HTTP Errors
    """


class NotFound(TaboolaError):
    """
    404 HTTP Errors
    """


class ServerError(TaboolaError):
    """
    500 HTTP Errors
    """
