"""Deye SUN-8K-SG05LP3-EU-SM2 — three-phase hybrid LV solar inverter.

Also compatible with the SUN-5K, SUN-6K, and SUN-10K variants of the
SG05LP3-EU-SM2 series, which share the same Modbus register map.

Reference: Deye Modbus RTU V105.4-20240814
Default Slave ID: 1 (set under Advanced Function → Modbus SN on the display)
Recommended bridge: Waveshare RS485 to WiFi/ETH in Modbus TCP ⟺ RTU mode
"""

from __future__ import annotations

from ..inverter_def import ComputedRegisterDef, InverterDef, RegisterDef

INVERTER = InverterDef(
    key="deye_sun8k_sg05lp3",
    name="Deye SUN-xK-SG05LP3-EU-SM2",
    manufacturer="Deye",
    model="SUN-8K-SG05LP3-EU-SM2",
    temp_registers={540, 541, 586},
    registers=[
        # ── General state ─────────────────────────────────────────────────────
        RegisterDef("Run State", 500, "", 1, "uint16", None, None, "mdi:information"),
        # ── Grid ──────────────────────────────────────────────────────────────
        RegisterDef("Grid L1 Voltage", 598, "V", 0.1, "uint16", "voltage", "measurement", "mdi:flash"),
        RegisterDef("Grid L2 Voltage", 599, "V", 0.1, "uint16", "voltage", "measurement", "mdi:flash"),
        RegisterDef("Grid L3 Voltage", 600, "V", 0.1, "uint16", "voltage", "measurement", "mdi:flash"),
        RegisterDef("Grid L1 Power", 622, "W", 1, "int16", "power", "measurement", "mdi:transmission-tower"),
        RegisterDef("Grid L2 Power", 623, "W", 1, "int16", "power", "measurement", "mdi:transmission-tower"),
        RegisterDef("Grid L3 Power", 624, "W", 1, "int16", "power", "measurement", "mdi:transmission-tower"),
        RegisterDef(
            "Grid Total Power", 625, "W", 1, "int16", "power", "measurement", "mdi:transmission-tower"
        ),
        RegisterDef("Grid Frequency", 609, "Hz", 0.01, "uint16", "frequency", "measurement", "mdi:sine-wave"),
        # ── PV (solar generation) ─────────────────────────────────────────────
        RegisterDef("PV1 Power", 672, "W", 1, "uint16", "power", "measurement", "mdi:solar-power"),
        RegisterDef("PV2 Power", 673, "W", 1, "uint16", "power", "measurement", "mdi:solar-power"),
        RegisterDef("PV3 Power", 674, "W", 1, "uint16", "power", "measurement", "mdi:solar-power"),
        RegisterDef("PV4 Power", 675, "W", 1, "uint16", "power", "measurement", "mdi:solar-power"),
        RegisterDef(
            "PV1 Voltage", 676, "V", 0.1, "uint16", "voltage", "measurement", "mdi:solar-power-variant"
        ),
        RegisterDef(
            "PV1 Current", 677, "A", 0.1, "uint16", "current", "measurement", "mdi:solar-power-variant"
        ),
        RegisterDef(
            "PV2 Voltage", 678, "V", 0.1, "uint16", "voltage", "measurement", "mdi:solar-power-variant"
        ),
        RegisterDef(
            "PV2 Current", 679, "A", 0.1, "uint16", "current", "measurement", "mdi:solar-power-variant"
        ),
        # ── Inverter AC output ────────────────────────────────────────────────
        RegisterDef("Inverter L1 Power", 633, "W", 1, "int16", "power", "measurement", "mdi:lightning-bolt"),
        RegisterDef("Inverter L2 Power", 634, "W", 1, "int16", "power", "measurement", "mdi:lightning-bolt"),
        RegisterDef("Inverter L3 Power", 635, "W", 1, "int16", "power", "measurement", "mdi:lightning-bolt"),
        RegisterDef(
            "Inverter Total Power", 636, "W", 1, "int16", "power", "measurement", "mdi:lightning-bolt"
        ),
        RegisterDef("Inverter L1 Voltage", 627, "V", 0.1, "uint16", "voltage", "measurement", "mdi:flash"),
        RegisterDef("Inverter L2 Voltage", 628, "V", 0.1, "uint16", "voltage", "measurement", "mdi:flash"),
        RegisterDef("Inverter L3 Voltage", 629, "V", 0.1, "uint16", "voltage", "measurement", "mdi:flash"),
        # ── Load (consumption) ────────────────────────────────────────────────
        RegisterDef("Load L1 Power", 650, "W", 1, "int16", "power", "measurement", "mdi:home-lightning-bolt"),
        RegisterDef("Load L2 Power", 651, "W", 1, "int16", "power", "measurement", "mdi:home-lightning-bolt"),
        RegisterDef("Load L3 Power", 652, "W", 1, "int16", "power", "measurement", "mdi:home-lightning-bolt"),
        RegisterDef(
            "Load Total Power", 653, "W", 1, "int16", "power", "measurement", "mdi:home-lightning-bolt"
        ),
        # ── Battery ───────────────────────────────────────────────────────────
        RegisterDef("Battery SOC", 588, "%", 1, "uint16", "battery", "measurement", "mdi:battery"),
        RegisterDef("Battery Voltage", 587, "V", 0.01, "uint16", "voltage", "measurement", "mdi:battery"),
        RegisterDef("Battery Current", 591, "A", 0.01, "int16", "current", "measurement", "mdi:battery"),
        RegisterDef("Battery Power", 590, "W", 1, "int16", "power", "measurement", "mdi:battery"),
        RegisterDef(
            "Battery Temperature", 586, "°C", 0.1, "uint16", "temperature", "measurement", "mdi:thermometer"
        ),
        # ── Temperature ───────────────────────────────────────────────────────
        RegisterDef(
            "DC Transformer Temp", 540, "°C", 0.1, "uint16", "temperature", "measurement", "mdi:thermometer"
        ),
        RegisterDef(
            "Heat Sink Temp", 541, "°C", 0.1, "uint16", "temperature", "measurement", "mdi:thermometer"
        ),
        # ── Daily energy counters ─────────────────────────────────────────────
        RegisterDef(
            "Today Generation", 529, "kWh", 0.1, "uint16", "energy", "total_increasing", "mdi:solar-power"
        ),
        RegisterDef(
            "Today Grid Buy",
            520,
            "kWh",
            0.1,
            "uint16",
            "energy",
            "total_increasing",
            "mdi:transmission-tower-import",
        ),
        RegisterDef(
            "Today Grid Sell",
            521,
            "kWh",
            0.1,
            "uint16",
            "energy",
            "total_increasing",
            "mdi:transmission-tower-export",
        ),
        RegisterDef(
            "Today Load", 526, "kWh", 0.1, "uint16", "energy", "total_increasing", "mdi:home-lightning-bolt"
        ),
        RegisterDef(
            "Today Battery Charge",
            514,
            "kWh",
            0.1,
            "uint16",
            "energy",
            "total_increasing",
            "mdi:battery-arrow-up",
        ),
        RegisterDef(
            "Today Battery Discharge",
            515,
            "kWh",
            0.1,
            "uint16",
            "energy",
            "total_increasing",
            "mdi:battery-arrow-down",
        ),
        # ── External CT (CT01 LoRa) ───────────────────────────────────────────
        RegisterDef(
            "External CT1 Current", 613, "A", 0.01, "int16", "current", "measurement", "mdi:current-ac"
        ),
        RegisterDef(
            "External CT2 Current", 614, "A", 0.01, "int16", "current", "measurement", "mdi:current-ac"
        ),
        RegisterDef(
            "External CT3 Current", 615, "A", 0.01, "int16", "current", "measurement", "mdi:current-ac"
        ),
        RegisterDef(
            "External CT1 Power", 616, "W", 1, "int16", "power", "measurement", "mdi:transmission-tower"
        ),
        RegisterDef(
            "External CT2 Power", 617, "W", 1, "int16", "power", "measurement", "mdi:transmission-tower"
        ),
        RegisterDef(
            "External CT3 Power", 618, "W", 1, "int16", "power", "measurement", "mdi:transmission-tower"
        ),
        RegisterDef(
            "External Total Power", 619, "W", 1, "int16", "power", "measurement", "mdi:transmission-tower"
        ),
    ],
    computed_registers=[
        # Sum of all active PV strings (None values from disconnected inputs are ignored)
        ComputedRegisterDef(
            name="PV Total Power",
            unit="W",
            device_class="power",
            state_class="measurement",
            icon="mdi:solar-power",
            sources=["PV1 Power", "PV2 Power", "PV3 Power", "PV4 Power"],
        ),
    ],
    # Explicit read blocks optimised for the Waveshare RS485-to-WiFi bridge.
    # Defined manually to avoid unnecessary reads across large address gaps
    # (e.g. the unused register 589 inside the battery block 586-591).
    read_blocks=[
        (500, 1),  # Run State
        (514, 2),  # Today Battery Charge / Discharge
        (520, 2),  # Today Grid Buy / Sell
        (526, 1),  # Today Load
        (529, 1),  # Today Generation
        (540, 2),  # DC Transformer Temp / Heat Sink Temp
        (586, 6),  # Battery block (586-591, gap at 589)
        (598, 3),  # Grid L1/L2/L3 Voltage
        (609, 1),  # Grid Frequency
        (613, 7),  # External CT (613-619)
        (622, 4),  # Grid L1/L2/L3 Power + Total
        (627, 3),  # Inverter L1/L2/L3 Voltage
        (633, 4),  # Inverter L1/L2/L3 Power + Total
        (650, 4),  # Load L1/L2/L3 Power + Total
        (672, 8),  # PV1-4 Power + PV1/PV2 Voltage/Current
    ],
)
