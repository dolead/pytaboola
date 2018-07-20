import re
import json
from datetime import date, datetime

import dateutil.parser

from pytaboola.errors import (BadRequest, Unauthorized,
                              TaboolaError, ServerError, NotFound)

ERROR_MAPPING = {
    400: BadRequest,
    401: Unauthorized,
    404: NotFound,
    500: ServerError,
}

DATE_FIELDS = (
    'start_date',
    'end_date',
)


def __cast_as_date(element):
    if isinstance(element, list):
        return [__cast_as_date(e) for e in element]
    return dateutil.parser.parse(element)


def __cast(item):
    if not isinstance(item, dict):
        return item
    new_item = item.copy()
    for key, value in item.items():
        if key in DATE_FIELDS and value:
            new_item[key] = __cast_as_date(value)
        elif isinstance(value, dict):
            new_item[key] = __cast(value)
        else:
            new_item[key] = value
    return new_item


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
            json_response = response.json()
            if 'errors' in json_response:
                error = json_response.get('errors')
            else:
                error = json_response.get('message')

        raise ERROR_MAPPING.get(response.status_code, TaboolaError)(error,
                                                                    response)
    return __cast(response.json())


def json_payload_formatter(obj):
    if isinstance(obj, datetime):
        return obj.date().isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, set):
        return list(obj)
    return obj
