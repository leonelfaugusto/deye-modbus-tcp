from __future__ import annotations

import asyncio

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry

from .const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_SLAVE,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SLAVE,
    DOMAIN,
)

STEP_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.All(int, vol.Range(min=1, max=65535)),
        vol.Required(CONF_SLAVE, default=DEFAULT_SLAVE): vol.All(int, vol.Range(min=1, max=247)),
        vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            int, vol.Range(min=5, max=300)
        ),
    }
)


async def _test_connection(host: str, port: int) -> str | None:
    """Verifica apenas se o TCP está acessível. Devolve chave de erro ou None."""
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=5.0
        )
        writer.close()
        await writer.wait_closed()
    except (OSError, asyncio.TimeoutError):
        return "cannot_connect"
    return None


class DeyeModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @config_entries.callback
    def async_get_options_flow(config_entry: ConfigEntry) -> DeyeModbusOptionsFlow:
        return DeyeModbusOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}

        if user_input is not None:
            error = await _test_connection(
                user_input[CONF_HOST],
                user_input[CONF_PORT],
            )
            if error:
                errors["base"] = error
            else:
                await self.async_set_unique_id(
                    f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Deye @ {user_input[CONF_HOST]}",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                STEP_SCHEMA, user_input or {}
            ),
            errors=errors,
        )


class DeyeModbusOptionsFlow(config_entries.OptionsFlow):
    """Permite alterar as definições após a integração estar configurada."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        self._entry = config_entry

    async def async_step_init(self, user_input=None):
        errors: dict[str, str] = {}

        # Valores actuais: options sobrepõem data (retrocompatibilidade)
        current = {**self._entry.data, **self._entry.options}

        if user_input is not None:
            error = await _test_connection(
                user_input[CONF_HOST],
                user_input[CONF_PORT],
            )
            if error:
                errors["base"] = error
            else:
                # Agendar reload antes de retornar para que o HA aplique
                # as novas definições logo após guardar as opções.
                # Corre na próxima iteração do event loop, depois de
                # entry.options ser actualizado pelo flow manager.
                self.hass.async_create_task(
                    self.hass.config_entries.async_reload(self._entry.entry_id)
                )
                return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(STEP_SCHEMA, current),
            errors=errors,
        )
