from datetime import date, datetime
from unittest.mock import Mock, patch

import pytest

from pytaboola import TaboolaClient
from pytaboola.errors import (
    BadRequest,
    NotFound,
    ServerError,
    TaboolaError,
    Unauthorized,
)
from pytaboola.services import (
    AccountService,
    CampaignItemService,
    CampaignService,
    CampaignSummaryReport,
    CountryResourcesService,
    PlatformResourcesService,
)
from pytaboola.services.base import BaseService, CrudService
from pytaboola.services.report import ReportService
from pytaboola.utils import (
    ERROR_MAPPING,
    json_payload_formatter,
    parse_response,
)

BASE_URL = "https://backstage.taboola.com"


def make_response(
    status_code=200, json_data=None, text="", content_type="application/json"
):
    response = Mock()
    response.ok = 200 <= status_code < 300
    response.status_code = status_code
    response.headers = {"Content-Type": content_type}
    response.text = text
    response.json = Mock(return_value=json_data)
    return response


def make_client(**kwargs):
    kwargs.setdefault("access_token", "a-token")
    return TaboolaClient("a-client-id", **kwargs)


# errors


def test_error_str_carries_class_status_and_message():
    error = BadRequest("Unknown publisher", make_response(400))
    assert str(error) == "BadRequest [400]: Unknown publisher"


def test_error_keeps_error_and_response():
    response = make_response(404)
    error = NotFound("account", response)
    assert error.error == "account"
    assert error.response is response


def test_error_mapping_covers_the_documented_statuses():
    assert ERROR_MAPPING == {
        400: BadRequest,
        401: Unauthorized,
        404: NotFound,
        500: ServerError,
    }


# parse_response


def test_parse_response_returns_payload():
    assert parse_response(make_response(json_data={"results": [1, 2]})) == {
        "results": [1, 2]
    }


def test_parse_response_casts_date_fields():
    parsed = parse_response(
        make_response(
            json_data={
                "start_date": "2026-01-02",
                "end_date": ["2026-01-03", "2026-01-04"],
                "nested": {"start_date": "2026-01-05"},
                "name": "untouched",
            }
        )
    )
    assert parsed["start_date"] == datetime(2026, 1, 2)
    assert parsed["end_date"] == [datetime(2026, 1, 3), datetime(2026, 1, 4)]
    assert parsed["nested"]["start_date"] == datetime(2026, 1, 5)
    assert parsed["name"] == "untouched"


def test_parse_response_leaves_empty_date_fields_alone():
    parsed = parse_response(make_response(json_data={"start_date": None}))
    assert parsed["start_date"] is None


@pytest.mark.parametrize(
    "status_code,expected",
    [
        (400, BadRequest),
        (401, Unauthorized),
        (404, NotFound),
        (500, ServerError),
        (418, TaboolaError),
    ],
)
def test_parse_response_raises_the_mapped_error(status_code, expected):
    response = make_response(status_code, json_data={"message": "nope"})
    with pytest.raises(expected) as caught:
        parse_response(response)
    assert caught.value.error == "nope"
    assert caught.value.response is response


def test_parse_response_prefers_the_errors_key():
    with pytest.raises(BadRequest) as caught:
        parse_response(
            make_response(
                400,
                json_data={
                    "errors": ["first", "second"],
                    "message": "ignored",
                },
            )
        )
    assert caught.value.error == ["first", "second"]


def test_parse_response_reads_xml_error_description():
    with pytest.raises(Unauthorized) as caught:
        parse_response(
            make_response(
                401,
                text="<error><error_description>bad token"
                "</error_description></error>",
                content_type="application/xml",
            )
        )
    assert caught.value.error == "bad token"


def test_parse_response_falls_back_to_raw_xml_body():
    with pytest.raises(ServerError) as caught:
        parse_response(
            make_response(
                500, text="<html>boom</html>", content_type="application/xml"
            )
        )
    assert caught.value.error == "<html>boom</html>"


def test_parse_response_falls_back_to_raw_body_on_unknown_type():
    with pytest.raises(BadRequest) as caught:
        parse_response(
            make_response(400, text="plain boom", content_type="text/plain")
        )
    assert caught.value.error == "plain boom"


# json_payload_formatter


def test_json_payload_formatter():
    assert json_payload_formatter(datetime(2026, 1, 2, 3, 4)) == "2026-01-02"
    assert json_payload_formatter(date(2026, 1, 2)) == "2026-01-02"
    assert sorted(json_payload_formatter({"b", "a"})) == ["a", "b"]
    assert json_payload_formatter("untouched") == "untouched"


# client


def test_client_needs_a_secret_or_a_token():
    with pytest.raises(AssertionError):
        TaboolaClient("a-client-id")


def test_client_authenticates_with_the_secret_when_token_is_missing():
    with patch("pytaboola.client.requests.request") as request:
        request.return_value = make_response(
            json_data={"access_token": "fresh"}
        )
        client = TaboolaClient("a-client-id", client_secret="a-secret")
    assert client.access_token == "fresh"
    method, url = request.call_args[0]
    assert (method, url) == ("POST", f"{BASE_URL}/backstage/oauth/token")
    assert request.call_args[1]["data"] == {
        "client_id": "a-client-id",
        "client_secret": "a-secret",
        "grant_type": "client_credentials",
    }


def test_authorization_header_needs_a_token():
    client = make_client()
    client.access_token = None
    with pytest.raises(RuntimeError):
        _ = client.authorization_header


def test_execute_builds_url_and_headers():
    with patch("pytaboola.client.requests.request") as request:
        request.return_value = make_response(json_data={"ok": True})
        assert make_client().execute(
            "GET", "some/uri", query_params={"page": 2}
        ) == {"ok": True}
    method, url = request.call_args[0]
    kwargs = request.call_args[1]
    assert (method, url) == ("GET", f"{BASE_URL}/some/uri")
    assert kwargs["headers"] == {"Authorization": "Bearer a-token"}
    assert kwargs["params"] == {"page": 2}
    assert kwargs["data"] is None
    assert kwargs["timeout"] is None


def test_execute_sends_json_payloads_on_post():
    with patch("pytaboola.client.requests.request") as request:
        request.return_value = make_response(json_data={})
        make_client().execute("POST", "some/uri", name="a-campaign")
    kwargs = request.call_args[1]
    assert kwargs["headers"]["Content-Type"] == "application/json"
    assert kwargs["data"] == '{"name": "a-campaign"}'


def test_execute_forwards_the_configured_timeout():
    client = make_client()
    client.timeout = 30
    with patch("pytaboola.client.requests.request") as request:
        request.return_value = make_response(json_data={})
        client.execute("GET", "some/uri")
    assert request.call_args[1]["timeout"] == 30


def test_execute_refreshes_the_token_then_retries():
    with patch("pytaboola.client.requests.request") as request:
        request.side_effect = [
            make_response(401, json_data={"message": "expired"}),
            make_response(json_data={"access_token": "fresh"}),
            make_response(json_data={"ok": True}),
        ]
        client = make_client(
            client_secret="a-secret", refresh_token="a-refresh-token"
        )
        assert client.execute("GET", "some/uri") == {"ok": True}
    assert client.access_token == "fresh"
    assert request.call_count == 3


def test_execute_gives_up_after_one_refresh():
    with patch("pytaboola.client.requests.request") as request:
        request.side_effect = [
            make_response(401, json_data={"message": "expired"}),
            make_response(json_data={"access_token": "fresh"}),
            make_response(401, json_data={"message": "still expired"}),
        ]
        client = make_client(
            client_secret="a-secret", refresh_token="a-refresh-token"
        )
        with pytest.raises(Unauthorized):
            client.execute("GET", "some/uri")
    assert request.call_count == 3


# services


def test_base_service_build_uri():
    service = BaseService(Mock())
    assert service.build_uri() == "backstage/api/1.0/"
    assert service.build_uri("///items") == "backstage/api/1.0//items"


def test_crud_service_calls_through():
    client = Mock()
    client.execute.return_value = {"results": ["a-campaign"]}
    service = CrudService(client, "an-account")
    assert service.list() == ["a-campaign"]
    service.get("an-id")
    assert client.execute.call_args[0] == ("GET", "backstage/api/1.0//an-id")
    service.create(name="a-name")
    assert client.execute.call_args[0] == ("POST", "backstage/api/1.0/")
    assert client.execute.call_args[1]["name"] == "a-name"
    service.update("an-id", name="a-name")
    assert client.execute.call_args[0] == ("POST", "backstage/api/1.0//an-id")


def test_account_service_uri():
    assert AccountService(Mock()).build_uri() == (
        "backstage/api/1.0//users/current/allowed-accounts/"
    )


def test_campaign_service_uris():
    service = CampaignService(Mock(), "an-account")
    assert service.build_uri() == ("backstage/api/1.0//an-account/campaigns/")
    assert service.build_uri("/42") == (
        "backstage/api/1.0//an-account/campaigns//42"
    )


def test_campaign_item_service_uris():
    service = CampaignItemService(Mock(), "an-account", "a-campaign")
    assert service.build_uri() == (
        "backstage/api/1.0//an-account/campaigns/a-campaign/items/"
    )
    assert service.build_uri("children") == (
        "backstage/api/1.0//an-account/campaigns/a-campaign/items//children/"
    )


def test_campaign_item_service_children():
    client = Mock()
    service = CampaignItemService(client, "an-account", "a-campaign")
    service.child("an-item")
    assert client.execute.call_args[0][1].endswith("children/an-item/")
    service.update_child("an-item", name="a-name")
    assert client.execute.call_args[0][0] == "POST"
    assert client.execute.call_args[1]["name"] == "a-name"


def test_resource_service_uris():
    assert PlatformResourcesService(Mock()).build_uri() == (
        "backstage/api/1.0//resources/platforms"
    )
    client = Mock()
    CountryResourcesService(client).regions("fr")
    assert client.execute.call_args[0] == (
        "GET",
        "backstage/api/1.0//resources/countries/FR/regions",
    )


# reports


def test_report_service_must_be_subclassed():
    with pytest.raises(NotImplementedError):
        ReportService(Mock(), "an-account").fetch(
            "day", date(2026, 1, 1), date(2026, 1, 2)
        )


def test_report_rejects_an_unknown_dimension():
    service = CampaignSummaryReport(Mock(), "an-account")
    with pytest.raises(ValueError, match="is not allowed"):
        service.fetch("nope", date(2026, 1, 1), date(2026, 1, 2))


def test_report_requires_dates():
    service = CampaignSummaryReport(Mock(), "an-account")
    with pytest.raises(AssertionError):
        service.fetch("day", "2026-01-01", date(2026, 1, 2))


def test_report_fetch_builds_uri_and_filters():
    client = Mock()
    service = CampaignSummaryReport(client, "an-account")
    service.fetch(
        "day",
        datetime(2026, 1, 1, 12, 30),
        date(2026, 1, 31),
        campaign="a-campaign",
        unsupported="dropped",
    )
    method, uri = client.execute.call_args[0]
    assert (method, uri) == (
        "GET",
        "backstage/api/1.0//an-account/reports/campaign-summary"
        "/dimensions/day",
    )
    assert client.execute.call_args[1]["query_params"] == {
        "start_date": "2026-01-01",
        "end_date": "2026-01-31",
        "campaign": "a-campaign",
    }
