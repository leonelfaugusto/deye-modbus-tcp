from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_HOST, DOMAIN, REGISTERS
from .coordinator import DeyeModbusCoordinator

_DEVICE_CLASS_MAP = {
    "voltage": SensorDeviceClass.VOLTAGE,
    "current": SensorDeviceClass.CURRENT,
    "power": SensorDeviceClass.POWER,
    "energy": SensorDeviceClass.ENERGY,
    "battery": SensorDeviceClass.BATTERY,
    "temperature": SensorDeviceClass.TEMPERATURE,
    "frequency": SensorDeviceClass.FREQUENCY,
}

_STATE_CLASS_MAP = {
    "measurement": SensorStateClass.MEASUREMENT,
    "total_increasing": SensorStateClass.TOTAL_INCREASING,
    "total": SensorStateClass.TOTAL,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: DeyeModbusCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        DeyeModbusSensor(coordinator, entry, reg) for reg in REGISTERS
    )


class DeyeModbusSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: DeyeModbusCoordinator,
        entry: ConfigEntry,
        reg: tuple,
    ) -> None:
        super().__init__(coordinator)
        name, _address, unit, _scale, _dtype, device_class, state_class, icon = reg

        self._reg_name = name
        self._attr_name = f"Deye {name}"
        self._attr_unique_id = f"{entry.entry_id}_{name.lower().replace(' ', '_')}"
        self._attr_native_unit_of_measurement = unit or None
        self._attr_icon = icon
        self._attr_device_class = _DEVICE_CLASS_MAP.get(device_class) if device_class else None
        self._attr_state_class = _STATE_CLASS_MAP.get(state_class) if state_class else None
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Deye Inverter",
            manufacturer="Deye",
            model="SUN-8K-SG05LP3-EU-SM2",
            configuration_url=f"http://{entry.data[CONF_HOST]}",
        )

    @property
    def native_value(self):
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._reg_name)
