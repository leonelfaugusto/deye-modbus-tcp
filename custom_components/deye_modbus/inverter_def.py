"""Tipos base para definições de inversores."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import NamedTuple


class RegisterDef(NamedTuple):
    """Definição de um registo Modbus."""

    name: str
    address: int
    unit: str
    scale: float
    dtype: str          # "uint16" ou "int16"
    device_class: str | None
    state_class: str | None
    icon: str


@dataclass
class InverterDef:
    """Definição completa de um modelo de inversor.

    Campos obrigatórios: key, name, manufacturer, model, registers, temp_registers.
    read_blocks é opcional — se omitido é calculado automaticamente a partir
    dos endereços dos registos (agrupa endereços com gap ≤ 5).
    """

    key: str                        # identificador único, ex: "deye_sun8k_sg05lp3"
    name: str                       # nome no dropdown, ex: "Deye SUN-8K-SG05LP3-EU-SM2"
    manufacturer: str               # ex: "Deye"
    model: str                      # número de modelo, ex: "SUN-8K-SG05LP3-EU-SM2"
    registers: list[RegisterDef]
    temp_registers: set[int]        # endereços com offset de temperatura (raw - 1000) * scale
    read_blocks: list[tuple[int, int]] = field(default_factory=list)

    # calculado em __post_init__
    addr_map: dict[int, tuple[int, int]] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        if not self.read_blocks:
            self.read_blocks = _auto_blocks(self.registers)
        self.addr_map = {
            start + offset: (block_idx, offset)
            for block_idx, (start, count) in enumerate(self.read_blocks)
            for offset in range(count)
        }


def _auto_blocks(
    registers: list[RegisterDef], max_gap: int = 5
) -> list[tuple[int, int]]:
    """Agrupa endereços consecutivos em blocos de leitura.

    max_gap: gap máximo (em endereços) para incluir num mesmo bloco.
    Endereços intermédios não usados são lidos mas ignorados.
    """
    addresses = sorted({r.address for r in registers})
    if not addresses:
        return []

    blocks: list[tuple[int, int]] = []
    start = end = addresses[0]

    for addr in addresses[1:]:
        if addr - end <= max_gap:
            end = addr
        else:
            blocks.append((start, end - start + 1))
            start = end = addr

    blocks.append((start, end - start + 1))
    return blocks
