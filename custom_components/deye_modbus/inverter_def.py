"""Base types for inverter definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import NamedTuple


class RegisterDef(NamedTuple):
    """Definition of a single Modbus holding register."""

    name: str
    address: int
    unit: str
    scale: float
    dtype: str  # "uint16" or "int16"
    device_class: str | None
    state_class: str | None
    icon: str


class ComputedRegisterDef(NamedTuple):
    """A derived sensor computed from other registers (e.g. sum of PV strings).

    The coordinator sums the values listed in `sources`, ignoring any that
    are None (disconnected or unresponsive inputs).
    Shares the same display fields as RegisterDef so both types can be handled
    by the same sensor entity.
    """

    name: str
    unit: str
    device_class: str | None
    state_class: str | None
    icon: str
    sources: list[str]  # names of RegisterDef entries to sum


@dataclass
class InverterDef:
    """Complete definition of an inverter model.

    Required fields: key, name, manufacturer, model, registers, temp_registers.
    read_blocks is optional — if omitted it is auto-computed from the register
    addresses by grouping consecutive addresses with a gap of at most 5.
    computed_registers: derived sensors calculated after the Modbus read.
    """

    key: str  # unique slug, e.g. "deye_sun8k_sg05lp3"
    name: str  # displayed in the config flow dropdown
    manufacturer: str
    model: str  # exact model number, e.g. "SUN-8K-SG05LP3-EU-SM2"
    registers: list[RegisterDef]
    temp_registers: set[int]  # addresses using Deye temperature offset: (raw - 1000) * scale
    read_blocks: list[tuple[int, int]] = field(default_factory=list)
    computed_registers: list[ComputedRegisterDef] = field(default_factory=list)

    # populated by __post_init__
    addr_map: dict[int, tuple[int, int]] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        if not self.read_blocks:
            self.read_blocks = _auto_blocks(self.registers)
        self.addr_map = {
            start + offset: (block_idx, offset)
            for block_idx, (start, count) in enumerate(self.read_blocks)
            for offset in range(count)
        }


def _auto_blocks(registers: list[RegisterDef], max_gap: int = 5) -> list[tuple[int, int]]:
    """Group register addresses into contiguous read blocks.

    Addresses within max_gap of each other are merged into a single block.
    Intermediate unused addresses are read but their values are discarded.
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
