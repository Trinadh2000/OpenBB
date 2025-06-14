"""Upstox Equity Historical Model."""

# pylint: disable=unused-argument

from datetime import date as dateType
from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.equity_historical import (
    EquityHistoricalData,
    EquityHistoricalQueryParams,
)
from openbb_upstox.utils import _make_request
from pydantic import Field


class UpstoxEquityHistoricalQueryParams(EquityHistoricalQueryParams):
    """Upstox Equity Historical Query."""

    unit: str = Field(default="day", description="Time unit.")
    interval: int = Field(default=1, description="Candle interval.")

    __alias_dict__ = {"symbol": "instrument_key"}


class UpstoxEquityHistoricalData(EquityHistoricalData):
    """Upstox Equity Historical Data."""

    __alias_dict__ = {
        "date": 0,
        "open": 1,
        "high": 2,
        "low": 3,
        "close": 4,
        "volume": 5,
    }


class UpstoxEquityHistoricalFetcher(
    Fetcher[
        UpstoxEquityHistoricalQueryParams,
        List[UpstoxEquityHistoricalData],
    ]
):
    """Transform the query, extract and transform the data from Upstox."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> UpstoxEquityHistoricalQueryParams:
        """Transform query params."""
        return UpstoxEquityHistoricalQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: UpstoxEquityHistoricalQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[List[Any]]:
        """Extract data from Upstox."""
        token = credentials.get("upstox_access_token") if credentials else ""
        url = (
            "https://api.upstox.com/v3/historical-candle/"
            f"{query.symbol}/{query.unit}/{query.interval}/{query.end_date}/{query.start_date}"
        )
        data = await _make_request(url, token, **kwargs)
        return data.get("data", {}).get("candles", [])

    @staticmethod
    def transform_data(
        query: UpstoxEquityHistoricalQueryParams,
        data: List[List[Any]],
        **kwargs: Any,
    ) -> List[UpstoxEquityHistoricalData]:
        """Transform the data."""
        results = []
        for item in data:
            model = {
                "date": item[0],
                "open": item[1],
                "high": item[2],
                "low": item[3],
                "close": item[4],
                "volume": item[5] if len(item) > 5 else None,
            }
            results.append(model)
        return [UpstoxEquityHistoricalData.model_validate(r) for r in results]
