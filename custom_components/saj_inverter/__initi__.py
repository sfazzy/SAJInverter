"""SAJ inverter integration – Home Assistant (HACS)."""
from __future__ import annotations

import asyncio
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from const import DOMAIN
from coordinator import SAJCoordinator

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[str] = ["sensor"]


async def async_setup(hass, config):
    conf = config.get(DOMAIN)
    if not conf:
        return True
    coordinator = SAJCoordinator(hass, conf["host"])
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})["yaml"] = coordinator
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from UI flow or YAML."""
    coordinator = SAJCoordinator(hass, entry.data["host"])
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok