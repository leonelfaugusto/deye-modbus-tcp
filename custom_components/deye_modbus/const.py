DOMAIN = "deye_modbus"

CONF_HOST = "host"
CONF_PORT = "port"
CONF_SLAVE = "slave"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_HOST = "10.10.20.102"
DEFAULT_PORT = 8899
DEFAULT_SLAVE = 1
DEFAULT_SCAN_INTERVAL = 10

# Registos de temperatura com offset 1000 (raw - 1000) * scale
TEMP_REGISTERS = {540, 541, 586}

# (nome, endereço, unidade, scale, dtype, device_class, state_class, icon)
REGISTERS = [
    # Estado geral
    ("Run State",              500, "",    1,     "uint16", None,          None,               "mdi:information"),

    # Grid
    ("Grid L1 Voltage",        598, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:flash"),
    ("Grid L2 Voltage",        599, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:flash"),
    ("Grid L3 Voltage",        600, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:flash"),
    ("Grid L1 Power",          622, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
    ("Grid L2 Power",          623, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
    ("Grid L3 Power",          624, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
    ("Grid Total Power",       625, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
    ("Grid Frequency",         609, "Hz",  0.01,  "uint16", "frequency",   "measurement",      "mdi:sine-wave"),

    # PV
    ("PV1 Power",              672, "W",   1,     "uint16", "power",       "measurement",      "mdi:solar-power"),
    ("PV2 Power",              673, "W",   1,     "uint16", "power",       "measurement",      "mdi:solar-power"),
    ("PV3 Power",              674, "W",   1,     "uint16", "power",       "measurement",      "mdi:solar-power"),
    ("PV4 Power",              675, "W",   1,     "uint16", "power",       "measurement",      "mdi:solar-power"),
    ("PV1 Voltage",            676, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:solar-power-variant"),
    ("PV1 Current",            677, "A",   0.1,   "uint16", "current",     "measurement",      "mdi:solar-power-variant"),
    ("PV2 Voltage",            678, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:solar-power-variant"),
    ("PV2 Current",            679, "A",   0.1,   "uint16", "current",     "measurement",      "mdi:solar-power-variant"),

    # Inversor
    ("Inverter L1 Power",      633, "W",   1,     "int16",  "power",       "measurement",      "mdi:lightning-bolt"),
    ("Inverter L2 Power",      634, "W",   1,     "int16",  "power",       "measurement",      "mdi:lightning-bolt"),
    ("Inverter L3 Power",      635, "W",   1,     "int16",  "power",       "measurement",      "mdi:lightning-bolt"),
    ("Inverter Total Power",   636, "W",   1,     "int16",  "power",       "measurement",      "mdi:lightning-bolt"),
    ("Inverter L1 Voltage",    627, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:flash"),
    ("Inverter L2 Voltage",    628, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:flash"),
    ("Inverter L3 Voltage",    629, "V",   0.1,   "uint16", "voltage",     "measurement",      "mdi:flash"),

    # Load
    ("Load L1 Power",          650, "W",   1,     "int16",  "power",       "measurement",      "mdi:home-lightning-bolt"),
    ("Load L2 Power",          651, "W",   1,     "int16",  "power",       "measurement",      "mdi:home-lightning-bolt"),
    ("Load L3 Power",          652, "W",   1,     "int16",  "power",       "measurement",      "mdi:home-lightning-bolt"),
    ("Load Total Power",       653, "W",   1,     "int16",  "power",       "measurement",      "mdi:home-lightning-bolt"),

    # Bateria
    ("Battery SOC",            588, "%",   1,     "uint16", "battery",     "measurement",      "mdi:battery"),
    ("Battery Voltage",        587, "V",   0.01,  "uint16", "voltage",     "measurement",      "mdi:battery"),
    ("Battery Current",        591, "A",   0.01,  "int16",  "current",     "measurement",      "mdi:battery"),
    ("Battery Power",          590, "W",   1,     "int16",  "power",       "measurement",      "mdi:battery"),
    ("Battery Temperature",    586, "°C",  0.1,   "uint16", "temperature", "measurement",      "mdi:thermometer"),

    # Temperatura
    ("DC Transformer Temp",    540, "°C",  0.1,   "uint16", "temperature", "measurement",      "mdi:thermometer"),
    ("Heat Sink Temp",         541, "°C",  0.1,   "uint16", "temperature", "measurement",      "mdi:thermometer"),

    # Energia diária
    ("Today Generation",       529, "kWh", 0.1,   "uint16", "energy",      "total_increasing", "mdi:solar-power"),
    ("Today Grid Buy",         520, "kWh", 0.1,   "uint16", "energy",      "total_increasing", "mdi:transmission-tower-import"),
    ("Today Grid Sell",        521, "kWh", 0.1,   "uint16", "energy",      "total_increasing", "mdi:transmission-tower-export"),
    ("Today Load",             526, "kWh", 0.1,   "uint16", "energy",      "total_increasing", "mdi:home-lightning-bolt"),
    ("Today Battery Charge",   514, "kWh", 0.1,   "uint16", "energy",      "total_increasing", "mdi:battery-arrow-up"),
    ("Today Battery Discharge",515, "kWh", 0.1,   "uint16", "energy",      "total_increasing", "mdi:battery-arrow-down"),

    # CT externo
    ("External CT1 Current",   613, "A",   0.01,  "int16",  "current",     "measurement",      "mdi:current-ac"),
    ("External CT2 Current",   614, "A",   0.01,  "int16",  "current",     "measurement",      "mdi:current-ac"),
    ("External CT3 Current",   615, "A",   0.01,  "int16",  "current",     "measurement",      "mdi:current-ac"),
    ("External CT1 Power",     616, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
    ("External CT2 Power",     617, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
    ("External CT3 Power",     618, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
    ("External Total Power",   619, "W",   1,     "int16",  "power",       "measurement",      "mdi:transmission-tower"),
]
