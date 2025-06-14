"""Upstox helper utilities."""

from typing import Dict

from openbb_core.provider.utils.helpers import amake_request


def _get_headers(access_token: str) -> Dict[str, str]:
    """Return request headers for Upstox."""
    return {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json",
    }


async def _make_request(url: str, access_token: str, **kwargs):
    """Wrapper around ``amake_request`` with default headers."""
    headers = _get_headers(access_token)
    return await amake_request(url, headers=headers, **kwargs)
