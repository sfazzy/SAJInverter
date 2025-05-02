"""SAJ inverter – network interface."""
from __future__ import annotations

import asyncio
import logging
import re
from typing import Final

import aiohttp
import async_timeout
from xml.etree import ElementTree as ET

_LOGGER = logging.getLogger(__name__)

PARAM_JS:   Final = "/param.js"
REALTIME:   Final = "/real_time_data.xml"
TIMEOUT:    Final = 10


class SAJApiError(RuntimeError):
    """Network or parse problem."""


class SAJApi:
    """Fetch order array (once) and live XML (repeat)."""

    def __init__(self, host: str, session: aiohttp.ClientSession) -> None:
        self._base = f"http://{host}"
        self._session = session
        self._order: list[str] | None = None

    # ------------------------------------------------------------------
    async def fetch(self) -> dict[str, float | int | str]:
        """Public: return dict keyed by DOM id (“v-pv1”, “p-ac”…)."""
        if self._order is None:           # first call → download param.js
            await self._load_order()

        values = await self._load_realtime()         # list[str]
        if len(values) != len(self._order):
            raise SAJApiError(
                f"Length mismatch: {len(values)} values vs {len(self._order)} ids"
            )

        return {
            name: self._auto(v)
            for name, v in zip(self._order, values, strict=False)
        }

    # ------------------------------------------------------------------
    async def _load_order(self) -> None:
        """Parse param.js → list of DOM ids in the order sent by XML."""
        text = await self._get_text(PARAM_JS)
        # Example line: var paraID=new Array("v-pv1","v-pv2",...);
        m = re.search(r'new Array\((.*?)\)', text, re.S)
        if not m:
            raise SAJApiError("Cannot find Array(...) in param.js")

        self._order = re.findall(r'"([^"]+)"', m.group(1))
        _LOGGER.debug("param.js order loaded: %s", self._order)

    async def _load_realtime(self) -> list[str]:
        """Return list of strings from <value>..</value>."""
        xml = await self._get_text(f"{REALTIME}?t=0")
        try:
            root = ET.fromstring(xml)
        except ET.ParseError as err:
            raise SAJApiError(err) from err

        return [e.text or "" for e in root.iter() if e.tag.lower() == "value"]

    # ------------------------------------------------------------------
    async def _get_text(self, path: str) -> str:
        """HTTP helper with timeout & logging."""
        url = f"{self._base}{path}"
        _LOGGER.debug("GET %s", url)
        try:
            async with async_timeout.timeout(TIMEOUT):
                async with self._session.get(url) as resp:
                    resp.raise_for_status()
                    return await resp.text()
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            raise SAJApiError(f"Request {url} failed: {err}") from err

    @staticmethod
    def _auto(value: str) -> float | int | str:
        """Convert numeric strings, leave others untouched."""
        v = value.strip()
        try:
            if "." in v:
                return float(v)
            return int(v)
        except ValueError:
            return v