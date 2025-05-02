"""Tiny async wrapper around SAJ /real_time_data.xml."""
from __future__ import annotations

import asyncio
from typing import Final

import aiohttp
import async_timeout
from xml.etree import ElementTree as ET

REALTIME: Final = "/real_time_data.xml"

class SAJApiError(RuntimeError):
    """Raised on network / parse problems."""

class SAJApi:
    def __init__(self, host: str, session: aiohttp.ClientSession) -> None:
        self._url = f"http://{host}{REALTIME}"
        self._session = session

    async def fetch(self) -> dict[str, float | int | str]:
        """Download and parse realtime XML."""
        try:
            async with async_timeout.timeout(10):
                async with self._session.get(self._url) as resp:
                    resp.raise_for_status()
                    text = await resp.text()
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            raise SAJApiError(err) from err

        try:
            tree = ET.fromstring(text)
        except ET.ParseError as err:
            raise SAJApiError(err) from err

        return {
            elem.tag: self._auto(elem.text)
            for elem in tree.iter()
            if elem.text and elem.tag != tree.tag
        }

    @staticmethod
    def _auto(value: str) -> float | int | str:
        """Convert strings to numbers when possible."""
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return value.strip()