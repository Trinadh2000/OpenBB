"""Upstox Equity Quote Model."""

# pylint: disable=unused-argument

from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.equity_quote import (
    EquityQuoteData,
    EquityQuoteQueryParams,
)
from openbb_upstox.utils import _make_request
from pydantic import Field


class UpstoxEquityQuoteQueryParams(EquityQuoteQueryParams):
    """Upstox Equity Quote Query."""

    __json_schema_extra__ = {"symbol": {"multiple_items_allowed": True}}


class UpstoxEquityQuoteData(EquityQuoteData):
    """Upstox Equity Quote Data."""

    __alias_dict__ = {
        "symbol": "symbol",
        "last_price": "ltp",
        "open": "open",
        "high": "high",
        "low": "low",
        "prev_close": "close",
    }


class UpstoxEquityQuoteFetcher(
    Fetcher[UpstoxEquityQuoteQueryParams, List[UpstoxEquityQuoteData]]
):
    """Upstox Equity Quote Fetcher."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> UpstoxEquityQuoteQueryParams:
        """Transform query params."""
        return UpstoxEquityQuoteQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: UpstoxEquityQuoteQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Extract data from Upstox."""
        token = credentials.get("upstox_access_token") if credentials else ""
        url = f"https://api.upstox.com/market-quote/ltp?symbol={query.symbol}"
        data = await _make_request(url, token, **kwargs)
        quotes = data.get("data", {})
        results = []
        for sym, quote in quotes.items():
            quote["symbol"] = sym
            results.append(quote)
        return results

    @staticmethod
    def transform_data(
        query: UpstoxEquityQuoteQueryParams,
        data: List[Dict],
        **kwargs: Any,
    ) -> List[UpstoxEquityQuoteData]:
        """Transform data."""
        return [UpstoxEquityQuoteData.model_validate(d) for d in data]
