"""Upstox Market Holidays Model."""

# pylint: disable=unused-argument

from datetime import date as dateType
from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.abstract.data import Data
from openbb_upstox.utils import _make_request
from pydantic import Field


class UpstoxMarketHolidaysQueryParams(QueryParams):
    """Market holidays query."""

    date: Optional[dateType] = Field(default=None, description="Specific date")


class UpstoxMarketHolidaysData(Data):
    """Market holidays data."""

    date: dateType = Field(description="Holiday date")
    description: str = Field(description="Holiday description")
    exchange: Optional[str] = Field(default=None, description="Exchange code")


class UpstoxMarketHolidaysFetcher(
    Fetcher[UpstoxMarketHolidaysQueryParams, List[UpstoxMarketHolidaysData]]
):
    """Market holidays fetcher."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> UpstoxMarketHolidaysQueryParams:
        """Transform query."""
        return UpstoxMarketHolidaysQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: UpstoxMarketHolidaysQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> Dict:
        """Extract data."""
        token = credentials.get("upstox_access_token") if credentials else ""
        if query.date:
            url = f"https://api.upstox.com/v2/market/holidays/{query.date}"
        else:
            url = "https://api.upstox.com/v2/market/holidays"
        return await _make_request(url, token, **kwargs)

    @staticmethod
    def transform_data(
        query: UpstoxMarketHolidaysQueryParams,
        data: Dict,
        **kwargs: Any,
    ) -> List[UpstoxMarketHolidaysData]:
        """Transform data."""
        records = data.get("data", [])
        results = []
        for item in records:
            results.append(
                {
                    "date": item.get("date"),
                    "description": item.get("description"),
                    "exchange": item.get("exchange"),
                }
            )
        return [UpstoxMarketHolidaysData.model_validate(r) for r in results]
