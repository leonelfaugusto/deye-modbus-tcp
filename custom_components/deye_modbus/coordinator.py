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
    CONF_INVERTER,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_SLAVE,
    DEFAULT_INVERTER,
    DOMAIN,
)
from .inverter_def import InverterDef
from .inverters import INVERTERS

_LOGGER = logging.getLogger(__name__)

_BLOCK_DELAY = 0.3


class DeyeModbusCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        opts = {**entry.data, **entry.options}
        self._host: str = opts[CONF_HOST]
        self._port: int = opts[CONF_PORT]
        self._slave: int = opts[CONF_SLAVE]
        self._inverter: InverterDef = INVERTERS[opts.get(CONF_INVERTER, DEFAULT_INVERTER)]

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=opts[CONF_SCAN_INTERVAL]),
        )

    @property
    def inverter(self) -> InverterDef:
        return self._inverter

    @property
    def host(self) -> str:
        return self._host

    async def _async_update_data(self) -> dict:
        client = AsyncModbusTcpClient(self._host, port=self._port)
        try:
            connected = await client.connect()
            if not connected:
                raise UpdateFailed("Falha ao ligar ao inversor")
            return await self._read_all_blocks(client)
        except UpdateFailed:
            raise
        except Exception as err:
            raise UpdateFailed(f"Erro inesperado: {err}") from err
        finally:
            client.close()

    async def _read_all_blocks(self, client: AsyncModbusTcpClient) -> dict:
        inv = self._inverter
        block_results: list = [None] * len(inv.read_blocks)

        for idx, (start, count) in enumerate(inv.read_blocks):
            try:
                result = await client.read_holding_registers(start, count=count)
                if result.isError():
                    _LOGGER.warning("Erro a ler bloco addr=%s count=%s", start, count)
                else:
                    block_results[idx] = result
            except ModbusException as err:
                _LOGGER.warning("Excepção Modbus no bloco addr=%s: %s", start, err)
            except Exception as err:
                _LOGGER.error("Erro inesperado no bloco addr=%s: %s", start, err)
            await asyncio.sleep(_BLOCK_DELAY)

        data: dict = {}
        for reg in inv.registers:
            block_info = inv.addr_map.get(reg.address)
            if block_info is None:
                data[reg.name] = None
                continue
            block_idx, offset = block_info
            result = block_results[block_idx]
            if result is None:
                data[reg.name] = None
                continue
            raw = result.registers[offset]
            if reg.dtype == "int16" and raw > 32767:
                raw -= 65536
            if reg.address in inv.temp_registers:
                data[reg.name] = round((raw - 1000) * reg.scale, 1)
            else:
                data[reg.name] = round(raw * reg.scale, 3)

        # Sensores derivados — calculados após leitura Modbus
        for computed in inv.computed_registers:
            values = [
                data[src]
                for src in computed.sources
                if data.get(src) is not None
            ]
            data[computed.name] = round(sum(values), 3) if values else None

        return data
