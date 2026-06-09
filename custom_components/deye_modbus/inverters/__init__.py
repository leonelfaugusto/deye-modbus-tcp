"""Registo de inversores suportados.

Para adicionar um novo inversor:
1. Cria um ficheiro nesta pasta (ex: deye_sun5k_sg03lp1.py)
2. Define um objecto INVERTER = InverterDef(...)
3. Importa-o aqui e adiciona-o à lista _ALL
"""
from __future__ import annotations

from ..inverter_def import InverterDef
from .deye_sun8k_sg05lp3 import INVERTER as _DEYE_SUN8K_SG05LP3

_ALL: list[InverterDef] = [
    _DEYE_SUN8K_SG05LP3,
]

# Dicionário chave → definição, usado pelo config flow e coordinator
INVERTERS: dict[str, InverterDef] = {inv.key: inv for inv in _ALL}
