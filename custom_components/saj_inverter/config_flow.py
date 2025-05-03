"""UI setup + options for SAJ inverter."""
from __future__ import annotations
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.helpers import logger as hass_logger

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
CONF_DEBUG = "debug_logging"

# -----------------------  CONFIG FLOW (first set‑up) --------------------------
class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)
        schema = vol.Schema({vol.Required(CONF_HOST): str})
        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_get_options_flow(self, entry):
        return OptionsFlowHandler(entry)

# ---------------------------  OPTIONS FLOW  -----------------------------------
class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, entry):       # entry = ConfigEntry
        self.entry = entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            # persist options
            return self.async_create_entry(title="", data=user_input)

        default = self.entry.options.get(CONF_DEBUG, False)
        schema = vol.Schema({vol.Optional(CONF_DEBUG, default=default): bool})
        return self.async_show_form(step_id="init", data_schema=schema)