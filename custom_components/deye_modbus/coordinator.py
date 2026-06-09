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
    CONF_SCAN_INTERVAL,
    CONF_SLAVE,
    DOMAIN,
    REGISTERS,
    TEMP_REGISTERS,
)

_LOGGER = logging.getLogger(__name__)

# Pausa entre leituras de blocos — o Waveshare precisa de tempo para
# encaminhar a resposta RTU de volta ao TCP antes do próximo pedido
_BLOCK_DELAY = 0.2

# Blocos de registos consecutivos — 15 transações em vez de 47.
# Registos com gap (ex: 589 na bateria) são lidos mas ignorados.
# (endereço_inicial, count)
_READ_BLOCKS: list[tuple[int, int]] = [
    (500, 1),   # Run State
    (514, 2),   # Today Battery Charge / Discharge
    (520, 2),   # Today Grid Buy / Sell
    (526, 1),   # Today Load
    (529, 1),   # Today Generation
    (540, 2),   # DC Transformer Temp / Heat Sink Temp
    (586, 6),   # Battery: Temp 586, Voltage 587, SOC 588, (589 gap), Power 590, Current 591
    (598, 3),   # Grid L1/L2/L3 Voltage
    (609, 1),   # Grid Frequency
    (613, 7),   # External CT (613–619)
    (622, 4),   # Grid L1/L2/L3 Power + Total
    (627, 3),   # Inverter L1/L2/L3 Voltage
    (633, 4),   # Inverter L1/L2/L3 Power + Total
    (650, 4),   # Load L1/L2/L3 Power + Total
    (672, 8),   # PV1–PV4 Power + PV1/PV2 Voltage/Current
]

# Mapa endereço → (índice do bloco, offset dentro do bloco)
_ADDR_MAP: dict[int, tuple[int, int]] = {
    start + offset: (block_idx, offset)
    for block_idx, (start, count) in enumerate(_READ_BLOCKS)
    for offset in range(count)
}


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
        try:
            client = await self._get_client()
        except Exception as err:
            raise UpdateFailed(f"Falha ao ligar ao inversor: {err}") from err

        # Ler cada bloco de registos consecutivos
        block_results: list = [None] * len(_READ_BLOCKS)
        for idx, (start, count) in enumerate(_READ_BLOCKS):
            try:
                result = await client.read_holding_registers(
                    start, count, self._slave
                )
                if result.isError():
                    _LOGGER.warning("Erro a ler bloco addr=%s count=%s", start, count)
                else:
                    block_results[idx] = result
            except ModbusException as err:
                _LOGGER.warning("Excepção Modbus no bloco addr=%s: %s", start, err)
            except Exception as err:
                _LOGGER.error("Erro inesperado no bloco addr=%s: %s", start, err)
            await asyncio.sleep(_BLOCK_DELAY)

        # Distribuir os valores pelos sensores a partir dos blocos lidos
        data: dict = {}
        for name, address, _unit, scale, dtype, *_ in REGISTERS:
            block_info = _ADDR_MAP.get(address)
            if block_info is None:
                _LOGGER.error("Endereço %s não está mapeado em nenhum bloco", address)
                data[name] = None
                continue
            block_idx, offset = block_info
            result = block_results[block_idx]
            if result is None:
                data[name] = None
                continue
            raw = result.registers[offset]
            if dtype == "int16" and raw > 32767:
                raw -= 65536
            if address in TEMP_REGISTERS:
                data[name] = round((raw - 1000) * scale, 1)
            else:
                data[name] = round(raw * scale, 3)

        return data

    async def async_shutdown(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
