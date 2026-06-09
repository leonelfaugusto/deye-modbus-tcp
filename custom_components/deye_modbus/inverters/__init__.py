"""Registry of supported inverter models.

To add a new inverter:
1. Create a file in this folder (e.g. my_brand_model.py)
2. Define an INVERTER = InverterDef(...) object
3. Import it here and append it to _ALL
"""
from __future__ import annotations

from ..inverter_def import InverterDef
from .deye_sun8k_sg05lp3 import INVERTER as _DEYE_SUN8K_SG05LP3

_ALL: list[InverterDef] = [
    _DEYE_SUN8K_SG05LP3,
]

# key → InverterDef mapping used by the config flow and coordinator
INVERTERS: dict[str, InverterDef] = {inv.key: inv for inv in _ALL}
