"""Upstox provider module."""

from openbb_core.provider.abstract.provider import Provider
from openbb_upstox.models.equity_historical import UpstoxEquityHistoricalFetcher
from openbb_upstox.models.equity_quote import UpstoxEquityQuoteFetcher
from openbb_upstox.models.options_chain import UpstoxOptionsChainsFetcher
from openbb_upstox.models.market_status import UpstoxMarketStatusFetcher
from openbb_upstox.models.market_holidays import UpstoxMarketHolidaysFetcher

upstox_provider = Provider(
    name="upstox",
    website="https://upstox.com",
    description="""Upstox provides trading APIs for Indian markets.""",
    credentials=["access_token"],
    fetcher_dict={
        "EquityHistorical": UpstoxEquityHistoricalFetcher,
        "EquityQuote": UpstoxEquityQuoteFetcher,
        "OptionsChains": UpstoxOptionsChainsFetcher,
        "MarketStatus": UpstoxMarketStatusFetcher,
        "MarketHolidays": UpstoxMarketHolidaysFetcher,
    },
    repr_name="Upstox",
)
