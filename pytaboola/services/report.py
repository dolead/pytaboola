import logging
from datetime import datetime, date

from pytaboola.services.base import AccountScopedService


logger = logging.getLogger(__name__)


class ReportService(AccountScopedService):
    report_name = None

    allowed_dimensions = ()

    allowed_filters = ()

    def __prepare_filters(self, start, end, **filters):
        assert isinstance(start, (datetime, date)), \
            "Start date filter must be a date/datetime instance"
        assert isinstance(end, (datetime, date)), \
            "End date filter must be a date/datetime instance"

        if isinstance(start, datetime):
            start = start.date()
        if isinstance(end, datetime):
            end = end.date()

        f = {'start_date': start.isoformat(),
             'end_date': end.isoformat()}

        for key, value in filters.items():
            if key in self.allowed_filters:
                f[key] = value
            else:
                logger.debug('%s is not allowed as a filter for %s',
                             key, self.__class__.__name__)
        return f

    def build_uri(self, dimension=None):
        endpoint = '{}/reports/{}/dimensions/{}'.format(
            self.account_id, self.report_name, dimension)
        return super().build_uri(endpoint)

    def fetch(self, dimension, start_date, end_date, **filters):
        if not self.report_name:
            raise NotImplementedError('ReportService must be subclassed')
        if dimension not in self.allowed_dimensions:
            raise ValueError('Dimension %s is not allowed for %s. '
                             'Must be one of %s' % (dimension,
                             self.__class__.__name__,
                             self.allowed_dimensions))

        real_filters = self.__prepare_filters(start_date, end_date, **filters)

        return self.execute('GET', self.build_uri(dimension),
                            query_params=real_filters)


class CampaignSummaryReport(ReportService):
    report_name = 'campaign-summary'

    allowed_dimensions = (
            'day', 'week', 'month', 'content_provider_breakdown',
            'campaign_breakdown', 'site_breakdown', 'country_breakdown',
            'platform_breakdown', 'campaign_day_breakdown',
            'campaign_site_day_breakdown',
    )

    allowed_filters = ('campaign', 'platform', 'country', 'site')


class TopCampaignContentReport(ReportService):
    report_name = 'top-campaign-content'

    allowed_dimensions = ('item_breakdown', )

    allowed_filters = ('campaign', )


class RevenueSummaryReport(ReportService):
    report_name = 'revenue-summary'

    allowed_dimensions = (
            'day', 'week', 'month', 'page_type_breakdown',
            'placement_breakdown', 'site_breakdown', 'country_breakdown',
            'platform_breakdown', 'day_site_placement_breakdown',
            'day_site_placement_country_platform_breakdown',
            'day_site_page_type_country_platform_breakdown',
    )

    allowed_filters = ('page_type', 'placement', 'country', 'platform')


class VisitValueReport(ReportService):
    report_name = 'visit-value'

    allowed_dimensions = (
            'day', 'week', 'month', 'by_referral', 'landing_page_breakdown',
            'platform_breakdown', 'country_breakdown', 'page_type_breakdown',
            'day_referral_landing_page_breakdown', 'by_source_medium',
            'by_campaign', 'by_custom_tracking_code',
            'by_referral_and_tracking_code',
    )

    allowed_filters = (
            'referral_domain', 'landing_page', 'country',
            'platform', 'campaign_source', 'campaign_medium',
            'campaign_term', 'campaign_content', 'campaign_name',
            'custom_key', 'custom_value', 'page_type',
    )


class RecirculationSummaryReport(ReportService):
    report_name = 'recirc-summary'

    allowed_dimensions = (
            'day', 'week', 'month', 'page_type_breakdown',
            'placement_breakdown', 'site_breakdown', 'country_breakdown',
            'platform_breakdown', 'day_site_placement_breakdown',
    )

    allowed_filters = (
            'page_type', 'placement', 'country', 'platform',
    )
