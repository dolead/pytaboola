import re

from pytaboola.errors import (BadRequest, Unauthorized,
                              TaboolaError, ServerError, NotFound)

ERROR_MAPPING = {
    400: BadRequest,
    401: Unauthorized,
    404: NotFound,
    500: ServerError,
}


def parse_response(response):
    if not response.ok:
        error = response.text
        if 'application/xml' in response.headers['Content-Type']:
            error = re.search(
                '<error_description>(.*)</error_description>',
                error, re.IGNORECASE)
            if error:
                error = error.group(1)
            else:
                error = response.text
        elif 'application/json' in response.headers['Content-Type']:
            error = response.json().get('errors')

        raise ERROR_MAPPING.get(response.status_code, TaboolaError)(error,
                                                                    response)
    return response.json()
