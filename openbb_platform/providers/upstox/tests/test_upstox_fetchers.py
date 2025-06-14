"""Upstox Fetchers Tests."""

from datetime import date

import pytest
from openbb_core.app.service.user_service import UserService
from openbb_upstox.models.equity_historical import UpstoxEquityHistoricalFetcher
from openbb_upstox.models.equity_quote import UpstoxEquityQuoteFetcher
from openbb_upstox.models.options_chain import UpstoxOptionsChainsFetcher
from openbb_upstox.models.market_status import UpstoxMarketStatusFetcher
from openbb_upstox.models.market_holidays import UpstoxMarketHolidaysFetcher


def _mock_request(url, token, **kwargs):
    if "ltp" in url:
        return {
            "data": {
                "NSE_EQ|RELIANCE": {
                    "ltp": 2500,
                    "open": 2450,
                    "high": 2550,
                    "low": 2440,
                    "close": 2480,
                }
            }
        }
    if "historical-candle" in url:
        return {"data": {"candles": [["2024-01-01", 1, 2, 0, 1, 100]]}}
    if "option/chain" in url:
        return {
            "data": [
                {
                    "expiry": "2024-02-01",
                    "strike_price": 100.0,
                    "underlying_key": "NSE_EQ|RELIANCE",
                    "underlying_spot_price": 101.0,
                    "call_options": {
                        "instrument_key": "CALL",
                        "market_data": {"oi": 10, "volume": 1, "ltp": 1.0},
                        "option_greeks": {"delta": 0.1, "gamma": 0.1, "theta": 0.1, "vega": 0.1, "iv": 0.2},
                    },
                }
            ]
        }
    if "holidays" in url:
        return {
            "data": [
                {"date": "2024-01-26", "description": "Republic Day", "exchange": "NSE"}
            ]
        }
    if "status" in url:
        return {"data": {"is_market_open": False, "timestamp": "2024-01-01"}}
    return {}


@pytest.fixture(autouse=True)
def patch_request(monkeypatch):
    async def _mock_async(*a, **k):
        return _mock_request(*a, **k)
    for module in [
        "openbb_upstox.models.equity_quote",
        "openbb_upstox.models.equity_historical",
        "openbb_upstox.models.options_chain",
        "openbb_upstox.models.market_status",
        "openbb_upstox.models.market_holidays",
    ]:
        monkeypatch.setattr(f"{module}._make_request", _mock_async)


test_credentials = UserService().default_user_settings.credentials.model_dump(mode="json")


@pytest.mark.record_http
def test_upstox_equity_quote_fetcher(credentials=test_credentials):
    params = {"symbol": "NSE_EQ|RELIANCE"}
    fetcher = UpstoxEquityQuoteFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_upstox_equity_historical_fetcher(credentials=test_credentials):
    params = {
        "symbol": "NSE_EQ|RELIANCE",
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 1, 2),
    }
    fetcher = UpstoxEquityHistoricalFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_upstox_options_chain_fetcher(credentials=test_credentials):
    params = {"symbol": "NSE_EQ|RELIANCE"}
    fetcher = UpstoxOptionsChainsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_upstox_market_status_fetcher(credentials=test_credentials):
    params = {"exchange": "NSE"}
    fetcher = UpstoxMarketStatusFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_upstox_market_holidays_fetcher(credentials=test_credentials):
    params = {}
    fetcher = UpstoxMarketHolidaysFetcher()
    result = fetcher.test(params, credentials)
    assert result is None
