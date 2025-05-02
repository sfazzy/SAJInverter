from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.saj_inverter.const import DOMAIN
from custom_components.saj_inverter.coordinator import SAJCoordinator

_DESCRIPTION_OVERRIDES: dict[str, SensorEntityDescription] = {
    "p-ac": SensorEntityDescription(
        key="p-ac",
        name="Grid Total Power",
        native_unit_of_measurement="W",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-power",
    ),
    "e-today": SensorEntityDescription(
        key="e-today",
        name="Energy Today",
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:counter",
    ),
    # Add more overrides here to polish names/units.
}

class SAJSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SAJCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        self.entity_description = description
        self.coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_{description.key}"

    @callback
    def _handle_coordinator_update(self) -> None:
        self._attr_native_value = self.coordinator.data.get(self.entity_description.key)
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        self._handle_coordinator_update()
        self.coordinator.async_add_listener(self._handle_coordinator_update)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: SAJCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Build one sensor per key returned by API
    entities: list[SAJSensor] = []
    for key, value in coordinator.data.items():
        desc = _DESCRIPTION_OVERRIDES.get(
            key,
            SensorEntityDescription(
                key=key,
                name=key.replace("-", " ").title(),
            ),
        )
        entities.append(SAJSensor(coordinator, desc))

    async_add_entities(entities, update_before_add=True)