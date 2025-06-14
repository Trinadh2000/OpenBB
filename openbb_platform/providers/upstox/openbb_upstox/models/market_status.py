"""Upstox Market Status Model."""

# pylint: disable=unused-argument

from typing import Any, Dict, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.abstract.data import Data
from openbb_upstox.utils import _make_request
from pydantic import Field


class UpstoxMarketStatusQueryParams(QueryParams):
    """Market status query."""

    exchange: str = Field(description="Exchange code")


class UpstoxMarketStatusData(Data):
    """Market status data."""

    exchange: str = Field(description="Exchange code")
    is_open: bool = Field(description="Whether market is open")
    timestamp: Optional[str] = Field(default=None, description="Status timestamp")


class UpstoxMarketStatusFetcher(
    Fetcher[UpstoxMarketStatusQueryParams, UpstoxMarketStatusData]
):
    """Market status fetcher."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> UpstoxMarketStatusQueryParams:
        """Transform query."""
        return UpstoxMarketStatusQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: UpstoxMarketStatusQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> Dict:
        """Extract data."""
        token = credentials.get("upstox_access_token") if credentials else ""
        url = f"https://api.upstox.com/v2/market/status/{query.exchange}"
        return await _make_request(url, token, **kwargs)

    @staticmethod
    def transform_data(
        query: UpstoxMarketStatusQueryParams,
        data: Dict,
        **kwargs: Any,
    ) -> UpstoxMarketStatusData:
        """Transform data."""
        info = data.get("data", {})
        return UpstoxMarketStatusData.model_validate(
            {
                "exchange": query.exchange,
                "is_open": info.get("is_market_open"),
                "timestamp": info.get("timestamp"),
            }
        )
