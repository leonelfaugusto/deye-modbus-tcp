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

from .const import DOMAIN
from .coordinator import DeyeModbusCoordinator
from .inverter_def import ComputedRegisterDef, RegisterDef

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
    inv = coordinator.inverter
    async_add_entities(
        DeyeModbusSensor(coordinator, entry, reg) for reg in [*inv.registers, *inv.computed_registers]
    )


class DeyeModbusSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: DeyeModbusCoordinator,
        entry: ConfigEntry,
        reg: RegisterDef | ComputedRegisterDef,
    ) -> None:
        super().__init__(coordinator)
        inv = coordinator.inverter

        self._reg_name = reg.name
        self._attr_name = f"Deye {reg.name}"
        self._attr_unique_id = f"{entry.entry_id}_{reg.name.lower().replace(' ', '_')}"
        self._attr_native_unit_of_measurement = reg.unit or None
        self._attr_icon = reg.icon
        self._attr_device_class = _DEVICE_CLASS_MAP.get(reg.device_class) if reg.device_class else None
        self._attr_state_class = _STATE_CLASS_MAP.get(reg.state_class) if reg.state_class else None
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"{inv.manufacturer} Inverter",
            manufacturer=inv.manufacturer,
            model=inv.model,
            configuration_url=f"http://{coordinator.host}",
        )

    @property
    def native_value(self):
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._reg_name)
