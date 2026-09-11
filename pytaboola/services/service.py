import logging

from pytaboola.services.base import BaseService, CrudService

logger = logging.getLogger(__name__)


class AccountService(BaseService):
    endpoint = f"{BaseService.endpoint}/users/current/allowed-accounts/"

    def list(self):
        return self.execute("GET", self.build_uri())


class CampaignService(CrudService):

    def build_uri(self, endpoint=None):
        base_endpoint = f"{self.endpoint}/{self.account_id}/campaigns/"
        if not endpoint:
            return base_endpoint
        while endpoint.startswith("/"):
            endpoint = endpoint[1:]
        return f"{base_endpoint}/{endpoint}"


class CampaignItemService(CrudService):

    def __init__(self, client, account_id, campaign_id):
        super().__init__(client, account_id)
        self.campaign_id = campaign_id

    def build_uri(self, endpoint=None):
        base_endpoint = (
            f"{self.endpoint}/{self.account_id}"
            f"/campaigns/{self.campaign_id}/items/"
        )
        if not endpoint:
            return base_endpoint
        while endpoint.startswith("/"):
            endpoint = endpoint[1:]
        if not endpoint.endswith("/"):
            endpoint += "/"
        return f"{base_endpoint}/{endpoint}"

    def children(self):
        return self.execute("GET", self.build_uri("children"))

    def child(self, item_id):
        return self.execute("GET", self.build_uri(f"children/{item_id}"))

    def update_child(self, item_id, **attrs):
        return self.execute(
            "POST", self.build_uri(f"children/{item_id}"), **attrs
        )
