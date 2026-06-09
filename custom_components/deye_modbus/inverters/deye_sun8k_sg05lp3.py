"""Deye SUN-8K-SG05LP3-EU-SM2 — inversor solar híbrido trifásico LV.

Compatível também com as variantes SUN-5K/6K/10K-SG05LP3-EU-SM2
que partilham o mesmo mapa de registos Modbus RTU V105.4.

Referência: Deye Modbus RTU V105.4-20240814
Slave ID padrão: 1 (configurado em Advanced Function → Modbus SN)
Bridge recomendada: Waveshare RS485 to WiFi/ETH, modo Modbus TCP⟺RTU
"""
from __future__ import annotations

from ..inverter_def import InverterDef, RegisterDef

INVERTER = InverterDef(
    key="deye_sun8k_sg05lp3",
    name="Deye SUN-xK-SG05LP3-EU-SM2",
    manufacturer="Deye",
    model="SUN-8K-SG05LP3-EU-SM2",
    temp_registers={540, 541, 586},
    registers=[
        # ── Estado geral ──────────────────────────────────────────────────────
        RegisterDef("Run State",              500, "",    1,     "uint16", None,          None,               "mdi:information"),

        # ── Grid (rede eléctrica) ─────────────────────────────────────────────
        RegisterDef("Grid L1 Voltage",        598, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:flash"),
        RegisterDef("Grid L2 Voltage",        599, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:flash"),
        RegisterDef("Grid L3 Voltage",        600, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:flash"),
        RegisterDef("Grid L1 Power",          622, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
        RegisterDef("Grid L2 Power",          623, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
        RegisterDef("Grid L3 Power",          624, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
        RegisterDef("Grid Total Power",       625, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
        RegisterDef("Grid Frequency",         609, "Hz",  0.01,  "uint16", "frequency",   "measurement",      "mdi:sine-wave"),

        # ── PV (produção solar) ───────────────────────────────────────────────
        RegisterDef("PV1 Power",              672, "W",   1,     "uint16", "power",       "measurement",      "mdi:solar-power"),
        RegisterDef("PV2 Power",              673, "W",   1,     "uint16", "power",       "measurement",      "mdi:solar-power"),
        RegisterDef("PV3 Power",              674, "W",   1,     "uint16", "power",       "measurement",      "mdi:solar-power"),
        RegisterDef("PV4 Power",              675, "W",   1,     "uint16", "power",       "measurement",      "mdi:solar-power"),
        RegisterDef("PV1 Voltage",            676, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:solar-power-variant"),
        RegisterDef("PV1 Current",            677, "A",   0.1,   "uint16", "current",     "measurement",      "mdi:solar-power-variant"),
        RegisterDef("PV2 Voltage",            678, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:solar-power-variant"),
        RegisterDef("PV2 Current",            679, "A",   0.1,   "uint16", "current",     "measurement",      "mdi:solar-power-variant"),

        # ── Inversor (output AC) ──────────────────────────────────────────────
        RegisterDef("Inverter L1 Power",      633, "W",   1,     "int16",  "power",       "measurement",      "mdi:lightning-bolt"),
        RegisterDef("Inverter L2 Power",      634, "W",   1,     "int16",  "power",       "measurement",      "mdi:lightning-bolt"),
        RegisterDef("Inverter L3 Power",      635, "W",   1,     "int16",  "power",       "measurement",      "mdi:lightning-bolt"),
        RegisterDef("Inverter Total Power",   636, "W",   1,     "int16",  "power",       "measurement",      "mdi:lightning-bolt"),
        RegisterDef("Inverter L1 Voltage",    627, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:flash"),
        RegisterDef("Inverter L2 Voltage",    628, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:flash"),
        RegisterDef("Inverter L3 Voltage",    629, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:flash"),

        # ── Load (consumo) ────────────────────────────────────────────────────
        RegisterDef("Load L1 Power",          650, "W",   1,     "int16",  "power",       "measurement",      "mdi:home-lightning-bolt"),
        RegisterDef("Load L2 Power",          651, "W",   1,     "int16",  "power",       "measurement",      "mdi:home-lightning-bolt"),
        RegisterDef("Load L3 Power",          652, "W",   1,     "int16",  "power",       "measurement",      "mdi:home-lightning-bolt"),
        RegisterDef("Load Total Power",       653, "W",   1,     "int16",  "power",       "measurement",      "mdi:home-lightning-bolt"),

        # ── Bateria ───────────────────────────────────────────────────────────
        RegisterDef("Battery SOC",            588, "%",   1,     "uint16", "battery",     "measurement",      "mdi:battery"),
        RegisterDef("Battery Voltage",        587, "V",   0.01,  "uint16", "voltage",     "measurement",      "mdi:battery"),
        RegisterDef("Battery Current",        591, "A",   0.01,  "int16",  "current",     "measurement",      "mdi:battery"),
        RegisterDef("Battery Power",          590, "W",   1,     "int16",  "power",       "measurement",      "mdi:battery"),
        RegisterDef("Battery Temperature",    586, "°C",  0.1,   "uint16", "temperature", "measurement",      "mdi:thermometer"),

        # ── Temperatura ───────────────────────────────────────────────────────
        RegisterDef("DC Transformer Temp",    540, "°C",  0.1,   "uint16", "temperature", "measurement",      "mdi:thermometer"),
        RegisterDef("Heat Sink Temp",         541, "°C",  0.1,   "uint16", "temperature", "measurement",      "mdi:thermometer"),

        # ── Energia diária ────────────────────────────────────────────────────
        RegisterDef("Today Generation",       529, "kWh", 0.1,   "uint16", "energy",      "total_increasing", "mdi:solar-power"),
        RegisterDef("Today Grid Buy",         520, "kWh", 0.1,   "uint16", "energy",      "total_increasing", "mdi:transmission-tower-import"),
        RegisterDef("Today Grid Sell",        521, "kWh", 0.1,   "uint16", "energy",      "total_increasing", "mdi:transmission-tower-export"),
        RegisterDef("Today Load",             526, "kWh", 0.1,   "uint16", "energy",      "total_increasing", "mdi:home-lightning-bolt"),
        RegisterDef("Today Battery Charge",   514, "kWh", 0.1,   "uint16", "energy",      "total_increasing", "mdi:battery-arrow-up"),
        RegisterDef("Today Battery Discharge",515, "kWh", 0.1,   "uint16", "energy",      "total_increasing", "mdi:battery-arrow-down"),

        # ── CT externo (CT01 LoRa) ────────────────────────────────────────────
        RegisterDef("External CT1 Current",   613, "A",   0.01,  "int16",  "current",     "measurement",      "mdi:current-ac"),
        RegisterDef("External CT2 Current",   614, "A",   0.01,  "int16",  "current",     "measurement",      "mdi:current-ac"),
        RegisterDef("External CT3 Current",   615, "A",   0.01,  "int16",  "current",     "measurement",      "mdi:current-ac"),
        RegisterDef("External CT1 Power",     616, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
        RegisterDef("External CT2 Power",     617, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
        RegisterDef("External CT3 Power",     618, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
        RegisterDef("External Total Power",   619, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
    ],
    # Blocos de leitura optimizados para o Waveshare RS485-to-WiFi.
    # Definidos explicitamente para evitar leituras desnecessárias
    # nos gaps entre grupos de registos (ex: 589 na bateria).
    read_blocks=[
        (500, 1),   # Run State
        (514, 2),   # Today Battery Charge / Discharge
        (520, 2),   # Today Grid Buy / Sell
        (526, 1),   # Today Load
        (529, 1),   # Today Generation
        (540, 2),   # DC Transformer Temp / Heat Sink Temp
        (586, 6),   # Battery (586-591, gap em 589)
        (598, 3),   # Grid L1/L2/L3 Voltage
        (609, 1),   # Grid Frequency
        (613, 7),   # External CT (613-619)
        (622, 4),   # Grid L1/L2/L3 Power + Total
        (627, 3),   # Inverter L1/L2/L3 Voltage
        (633, 4),   # Inverter L1/L2/L3 Power + Total
        (650, 4),   # Load L1/L2/L3 Power + Total
        (672, 8),   # PV1-4 Power + PV1/PV2 Voltage/Current
    ],
)
