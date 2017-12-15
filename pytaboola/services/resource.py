import logging

from pytaboola.services.base import BaseService


logger = logging.getLogger(__name__)


class ResourcesService(BaseService):
    endpoint = '{}/{}'.format(BaseService.endpoint, 'resources')

    def list(self):
        return self.execute('GET', self.build_uri())


class PlatformResourcesService(ResourcesService):
    endpoint = '{}/{}'.format(ResourcesService.endpoint, 'platforms')


class CountryResourcesService(ResourcesService):
    endpoint = '{}/{}'.format(ResourcesService.endpoint, 'countries')

    def _elements(self, country, element):
        return self.execute('GET', self.build_uri('{}/{}'.format(country.upper(), element)))

    def regions(self, country):
        return self._elements(country, 'regions')

    def postal_codes(self, country):
        return self._elements(country, 'postal_codes')

    def dmas(self):
        return self._elements('US', 'postal_codes')


class CampaignPropertiesResourcesService(ResourcesService):
    endpoint = '{}/{}'.format(ResourcesService.endpoint, 'campaigns_properties')

    def elements(self, item):
        return self.execute('GET', self.build_uri(item))

    def item_properties(self):
        return self.execute('GET', self.build_uri('items_properties'))

    def item_property_elements(self, item):
        return self.execute('GET', self.build_uri('items_properties/{}'.format(item)))
