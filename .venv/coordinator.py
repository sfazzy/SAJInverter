from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, UPDATE_INTERVAL
from .api import SAJApi, SAJApiError

_LOGGER = logging.getLogger(__name__)

class SAJCoordinator(DataUpdateCoordinator[dict[str, float | int | str]]):
    def __init__(self, hass: HomeAssistant, host: str) -> None:
        self.api = SAJApi(host, aiohttp.ClientSession())
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, float | int | str]:
        try:
            return await self.api.fetch()
        except SAJApiError as err:
            raise UpdateFailed(err) from err