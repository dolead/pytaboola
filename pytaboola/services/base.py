import logging
from datetime import date, datetime


logger = logging.getLogger(__name__)


class BaseService:
    """
    Service class, expose calls

    """
    endpoint = 'backstage/api/1.0/'

    def __init__(self, client):
        self.client = client

    def build_uri(self, endpoint=None):
        if not endpoint:
            return self.endpoint
        while endpoint.startswith('/'):
            endpoint = endpoint[1:]
        return '{}/{}'.format(self.endpoint, endpoint)


    def execute(self, method, uri, query_params=None, **payload):
        return self.client.execute(method, uri,
                                   query_params=query_params, **payload)


class AccountScopedService(BaseService):

    def __init__(self, client, account_id):
        super().__init__(client)
        self.account_id = account_id


class CrudService(AccountScopedService):

    def list(self):
        return self.execute('GET', self.build_uri())['results']

    def get(self, element_id):
        return self.execute('GET', self.build_uri(element_id))

    def create(self, **attrs):
        return self.execute('POST', self.build_uri(), **attrs)

    def update(self, element_id, **attrs):
        return self.execute('POST', self.build_uri(element_id), **attrs)
