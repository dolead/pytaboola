import json
import logging
import requests

from pytaboola.errors import Unauthorized
from pytaboola.utils import parse_response

logger = logging.getLogger(__name__)


class TaboolaClient:
    """

    """

    base_url = 'https://backstage.taboola.com'

    def __init__(self, client_id, client_secret=None,
                 access_token=None, refresh_token=None):

        assert client_secret or access_token, "Must provide either the client secret or an access token"
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret

        if not self.access_token:
            self.refresh()

    @property
    def oauth_uri(self):
        return 'backstage/oauth/token'.format(self.base_url)

    def __authenticate_secret(self):
        logger.debug('Requesting access token with '
                     'client_id(%s)/client_secret', self.client_id)

        result = self.execute('POST', self.oauth_uri,
                              allow_refresh=False,
                              raw=True,
                              authenticated=False,
                              client_id=self.client_id,
                              client_secret=self.client_secret,
                              grant_type='client_credentials')

        logger.debug('Response is %s', result)
        self.access_token = result.get('access_token')


    def __authenticate_refresh(self):
        if not (self.refresh_token and self.client_secret):
            return

        logger.debug('Requesting access token with '
                     'client_id(%s)/refresh token(%s)',
                     self.client_id, self.refresh_token)

        result = self.execute('POST', self.oauth_uri,
                              allow_refresh=False,
                              raw=True,
                              authenticated=False,
                              client_id=self.client_id,
                              client_secret=self.client_secret,
                              refresh_token=self.refresh_token,
                              grant_type='refresh_token')

        logger.debug('Response is %s', result)
        self.access_token = result.get('access_token')


    def refresh(self):
        if self.refresh_token:
            self.__authenticate_refresh()
        if not self.access_token and self.client_secret:
            self.__authenticate_secret()

    @property
    def authorization_header(self):
        if not self.access_token:
            raise Exception
        return {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }

    @property
    def token_details(self):
        return self.execute('GET', 'backstage/api/1.0/token-details/')

    def execute(self, method, uri, query_params=None,
                allow_refresh=True, raw=False, authenticated=True,
                **payload):
        url = '{}/{}'.format(self.base_url, uri)
        headers = self.authorization_header if authenticated else {}
        if method.upper() in ('POST', 'PUT') and not raw:
            headers['Content-Type'] = 'application/json'

        try:
            data = None
            if payload:
                data = payload if raw else json.dumps(payload)
            result = requests.request(method, url, data=data,
                                      params=query_params,
                                      headers=headers)
            return parse_response(result)
        except Unauthorized:
            if not allow_refresh:
                raise
            self.refresh()
            return self.execute(method, uri, query_params=query_params,
                                raw=raw, allow_refresh=False, **payload)
