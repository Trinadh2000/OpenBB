"""Upstox Options Chain Model."""

# pylint: disable=unused-argument

from datetime import date as dateType
from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.options_chains import (
    OptionsChainsData,
    OptionsChainsQueryParams,
)
from openbb_upstox.utils import _make_request
from pydantic import Field


class UpstoxOptionsChainsQueryParams(OptionsChainsQueryParams):
    """Upstox Options Chains Query."""

    expiry: Optional[dateType] = Field(default=None, description="Expiry date")
    __alias_dict__ = {"symbol": "instrument_key"}


class UpstoxOptionsChainsData(OptionsChainsData):
    """Upstox Options Chains Data."""

    pass


class UpstoxOptionsChainsFetcher(
    Fetcher[UpstoxOptionsChainsQueryParams, UpstoxOptionsChainsData]
):
    """Upstox Options Chains Fetcher."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> UpstoxOptionsChainsQueryParams:
        """Transform query params."""
        return UpstoxOptionsChainsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: UpstoxOptionsChainsQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> Dict:
        """Extract data from Upstox."""
        token = credentials.get("upstox_access_token") if credentials else ""
        url = (
            "https://api.upstox.com/v2/option/chain?"
            f"instrument_key={query.symbol}&expiry_date={query.expiry}"
        )
        return await _make_request(url, token, **kwargs)

    @staticmethod
    def transform_data(
        query: UpstoxOptionsChainsQueryParams,
        data: Dict,
        **kwargs: Any,
    ) -> UpstoxOptionsChainsData:
        """Transform data into OptionsChainsData."""
        chains = []
        for strike in data.get("data", []):
            exp = strike.get("expiry")
            strike_price = strike.get("strike_price")
            underlying_key = strike.get("underlying_key")
            underlying_price = strike.get("underlying_spot_price")
            for option_type, record in {
                "call": strike.get("call_options"),
                "put": strike.get("put_options"),
            }.items():
                if not record:
                    continue
                md = record.get("market_data", {})
                greek = record.get("option_greeks", {})
                chains.append(
                    {
                        "underlying_symbol": underlying_key,
                        "underlying_price": underlying_price,
                        "contract_symbol": record.get("instrument_key"),
                        "expiration": exp,
                        "strike": strike_price,
                        "option_type": option_type,
                        "open_interest": md.get("oi"),
                        "volume": md.get("volume"),
                        "last_price": md.get("ltp"),
                        "bid": md.get("bid_price"),
                        "ask": md.get("ask_price"),
                        "delta": greek.get("delta"),
                        "gamma": greek.get("gamma"),
                        "theta": greek.get("theta"),
                        "vega": greek.get("vega"),
                        "implied_volatility": greek.get("iv"),
                    }
                )
        if not chains:
            empty = {field: [None] for field in UpstoxOptionsChainsData.model_fields}
            return UpstoxOptionsChainsData.model_validate(empty)
        return UpstoxOptionsChainsData.model_validate({k: [d[k] for d in chains] for k in chains[0]})
