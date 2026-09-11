class TaboolaError(Exception):
    """
    Base error class for handling Taboola backstage API errors

    Inherits Exception, not BaseException: an API error is an
    ordinary failure callers are meant to catch, and deriving it
    from BaseException made it slip through every `except
    Exception` -- taking the process down instead of the call.
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
