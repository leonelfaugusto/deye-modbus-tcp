from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SLAVE,
    CONF_SCAN_INTERVAL,
    DOMAIN,
    REGISTERS,
    TEMP_REGISTERS,
)

_LOGGER = logging.getLogger(__name__)

# Pausa entre leituras consecutivas para não saturar o Waveshare
_READ_DELAY = 0.05


class DeyeModbusCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self._host = entry.data[CONF_HOST]
        self._port = entry.data[CONF_PORT]
        self._slave = entry.data[CONF_SLAVE]
        self._client: AsyncModbusTcpClient | None = None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=entry.data[CONF_SCAN_INTERVAL]),
        )

    async def _get_client(self) -> AsyncModbusTcpClient:
        if self._client is None or not self._client.connected:
            if self._client is not None:
                self._client.close()
            self._client = AsyncModbusTcpClient(self._host, port=self._port)
            await self._client.connect()
        return self._client

    async def _async_update_data(self) -> dict:
        data: dict = {}
        try:
            client = await self._get_client()
        except Exception as err:
            raise UpdateFailed(f"Falha ao ligar ao inversor: {err}") from err

        for name, address, _unit, scale, dtype, *_ in REGISTERS:
            try:
                result = await client.read_holding_registers(
                    address=address, count=1, slave=self._slave
                )
                if result.isError():
                    _LOGGER.warning("Erro a ler registo %s (addr %s)", name, address)
                    data[name] = None
                else:
                    raw = result.registers[0]
                    if dtype == "int16" and raw > 32767:
                        raw = raw - 65536
                    if address in TEMP_REGISTERS:
                        data[name] = round((raw - 1000) * scale, 1)
                    else:
                        data[name] = round(raw * scale, 3)
            except ModbusException as err:
                _LOGGER.warning("Excepção Modbus em %s: %s", name, err)
                data[name] = None
            except Exception as err:
                _LOGGER.error("Erro inesperado em %s: %s", name, err)
                data[name] = None

            await asyncio.sleep(_READ_DELAY)

        return data

    async def async_shutdown(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
