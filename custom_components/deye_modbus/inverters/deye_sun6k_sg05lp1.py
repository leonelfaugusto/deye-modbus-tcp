from __future__ import annotations

from ..inverter_def import ComputedRegisterDef, InverterDef, RegisterDef

INVERTER = InverterDef(
    key="deye_sun6k_sg05lp1",
    name="Deye SUN-6K-SG05LP1 (Single Phase)",
    manufacturer="Deye",
    model="SUN-6K-SG05LP1",
    temp_registers={90},  # Температура DC
    registers=[
        # Справжні LP1-регістри для однофазників Deye:
        RegisterDef(
            "Inverter Temperature", 90, "°C", 0.1, "int16", "temperature", "measurement", "mdi:thermometer"
        ),
        RegisterDef("Battery Voltage", 183, "V", 0.01, "uint16", "voltage", "measurement", "mdi:flash"),
        RegisterDef("Battery SOC", 184, "%", 1, "uint16", "battery", "measurement", "mdi:battery"),
        RegisterDef("Battery Power", 190, "W", 1, "int16", "power", "measurement", "mdi:battery-charging"),
        RegisterDef("Battery Current", 191, "A", 0.01, "int16", "current", "measurement", "mdi:current-dc"),
        RegisterDef("Grid Voltage L1", 150, "V", 0.1, "uint16", "voltage", "measurement", "mdi:flash"),
        RegisterDef("Grid Frequency", 79, "Hz", 0.01, "uint16", "frequency", "measurement", "mdi:sine-wave"),
        RegisterDef("Grid Power", 169, "W", 1, "int16", "power", "measurement", "mdi:transmission-tower"),
        RegisterDef("Grid CT Power", 172, "W", 1, "int16", "power", "measurement", "mdi:transmission-tower"),
        RegisterDef("Load Power", 178, "W", 1, "uint16", "power", "measurement", "mdi:home-lightning-bolt"),
        RegisterDef("PV1 Power", 186, "W", 1, "uint16", "power", "measurement", "mdi:solar-power"),
        RegisterDef("PV2 Power", 187, "W", 1, "uint16", "power", "measurement", "mdi:solar-power"),
        RegisterDef("PV1 Voltage", 109, "V", 0.1, "uint16", "voltage", "measurement", "mdi:flash"),
        RegisterDef("PV2 Voltage", 111, "V", 0.1, "uint16", "voltage", "measurement", "mdi:flash"),
        RegisterDef(
            "Daily PV Energy",
            108,
            "kWh",
            0.1,
            "uint16",
            "energy",
            "total_increasing",
            "mdi:solar-power-variant",
        ),
        RegisterDef(
            "Daily Grid Import",
            76,
            "kWh",
            0.1,
            "uint16",
            "energy",
            "total_increasing",
            "mdi:transmission-tower-import",
        ),
        RegisterDef(
            "Daily Grid Export",
            77,
            "kWh",
            0.1,
            "uint16",
            "energy",
            "total_increasing",
            "mdi:transmission-tower-export",
        ),
        RegisterDef(
            "Daily Battery Charge",
            70,
            "kWh",
            0.1,
            "uint16",
            "energy",
            "total_increasing",
            "mdi:battery-arrow-up",
        ),
        RegisterDef(
            "Daily Battery Discharge",
            71,
            "kWh",
            0.1,
            "uint16",
            "energy",
            "total_increasing",
            "mdi:battery-arrow-down",
        ),
        RegisterDef(
            "Daily Load Energy",
            84,
            "kWh",
            0.1,
            "uint16",
            "energy",
            "total_increasing",
            "mdi:home-lightning-bolt",
        ),
    ],
    computed_registers=[
        ComputedRegisterDef(
            name="PV Total Power",
            unit="W",
            device_class="power",
            state_class="measurement",
            icon="mdi:solar-power",
            sources=["PV1 Power", "PV2 Power"],
        ),
    ],
    # Блоки читання для діапазону 0-299
    read_blocks=[
        (70, 2),  # Заряд та Розряд АКБ за сьогодні (70, 71)
        (76, 4),  # Імпорт/Експорт мережі (76, 77) та Частота мережі (79)
        (84, 1),  # Споживання будинку за сьогодні
        (90, 1),
        (108, 1),  # Генерація за сьогодні
        (109, 3),
        (150, 1),  # Grid Voltage L1 (150)
        (169, 4),
        (178, 1),
        (183, 2),
        (186, 2),
        (190, 2),
    ],
)
