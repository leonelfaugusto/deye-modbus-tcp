# Deye Modbus — Home Assistant Custom Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/v/release/leonelfaugusto/deye-modbus-tcp)](https://github.com/leonelfaugusto/deye-modbus-tcp/releases)
[![HA version](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-blue)](https://www.home-assistant.io/)

Home Assistant custom component that reads data from solar inverters via Modbus TCP, using a Waveshare RS485-to-WiFi adapter (or compatible) as a bridge.

---

## Supported inverters

| Model | File key | Phases | PV strings |
|---|---|---|---|
| Deye SUN-xK-SG05LP3-EU-SM2 | `deye_sun8k_sg05lp3` | 3 | 4 |

> Compatible with the SUN-5K, SUN-6K, SUN-8K and SUN-10K variants of the SG05LP3-EU-SM2 series, which share the same Modbus register map (RTU V105.4).

Want to add your inverter? See **[Contributing — Adding a new inverter](#contributing--adding-a-new-inverter)**.

---

## Tested hardware

| Component | Model |
|---|---|
| Inverter | Deye SUN-8K-SG05LP3-EU-SM2 |
| RS485 adapter | Waveshare RS485 to WiFi/ETH |

### Hardware requirements

- Waveshare configured in **Modbus TCP ⟺ Modbus RTU** mode (not Transparent)
- Inverter with **Modbus SN = 01** (set under Advanced Function on the inverter display)
- Baud rate: **9600 bps, 8N1** — must match on both the Waveshare and the inverter
- Do not use Transparent mode on the Waveshare — the TCP/RTU framing is different

---

## Installation via HACS

1. In HACS → Integrations → ⋮ → **Custom repositories**
2. Add `https://github.com/leonelfaugusto/deye-modbus-tcp`, category: **Integration**
3. Install **Deye Modbus**
4. Restart Home Assistant
5. Go to **Settings → Integrations → Add integration → Deye Modbus**

## Manual installation

Copy the `custom_components/deye_modbus/` folder to `<config>/custom_components/` and restart HA.

---

## Configuration

| Field | Default | Description |
|---|---|---|
| Inverter model | — | Select from the list of supported models |
| Host (IP) | `10.10.20.102` | IP address of the Waveshare adapter |
| TCP Port | `8899` | TCP port of the Waveshare adapter |
| Modbus Slave ID | `1` | Slave ID configured on the inverter |
| Polling interval | `10` | Seconds between reads (min. 5 s) |

### Changing settings after setup

Go to **Settings → Integrations → Deye Modbus → Configure**. All settings can be changed without losing sensor history.

---

## Sensors

The integration creates a single device with all sensors grouped under it.

### Deye SUN-xK-SG05LP3-EU-SM2 (48 sensors)

| Group | Sensors |
|---|---|
| General | Run State |
| Grid | L1/L2/L3 Voltage · L1/L2/L3 Power · Total Power · Frequency |
| PV | PV1–PV4 Power · PV1/PV2 Voltage · PV1/PV2 Current · **PV Total Power** ¹ |
| Inverter | L1/L2/L3 Power · Total Power · L1/L2/L3 Voltage |
| Load | L1/L2/L3 Power · Total Power |
| Battery | SOC · Voltage · Current · Power · Temperature |
| Temperature | DC Transformer Temp · Heat Sink Temp |
| Daily energy | Generation · Grid Buy · Grid Sell · Load · Battery Charge · Battery Discharge |
| External CT | CT1/CT2/CT3 Current · CT1/CT2/CT3 Power · Total Power |

¹ **PV Total Power** is automatically computed as the sum of all active PV strings (disconnected or unresponsive strings are ignored).

### Sign conventions

| Sensor | Positive value | Negative value |
|---|---|---|
| Grid Power | Importing from grid | Exporting to grid |
| Battery Power | Discharging | Charging |
| Battery Current | Discharging | Charging |

---

## Energy Dashboard

The following sensors are compatible with the Home Assistant Energy Dashboard (`state_class: total_increasing`):

- `Today Generation` → Solar production
- `Today Grid Buy` → Grid consumption
- `Today Grid Sell` → Grid export
- `Today Load` → Total house consumption
- `Today Battery Charge` → Battery charge energy
- `Today Battery Discharge` → Battery discharge energy

---

## Contributing — Adding a new inverter

The integration is designed to be easily extensible. Each inverter model is defined in a standalone Python file inside `custom_components/deye_modbus/inverters/`.

### Step 1 — Create the definition file

Create `custom_components/deye_modbus/inverters/<model_key>.py`:

```python
"""Brief description of the inverter and reference to the Modbus manual."""
from __future__ import annotations

from ..inverter_def import ComputedRegisterDef, InverterDef, RegisterDef

INVERTER = InverterDef(
    key="brand_model",              # unique slug, no spaces
    name="Brand Model-XYZ",        # shown in the config flow dropdown
    manufacturer="Brand",
    model="Model-XYZ",

    # Addresses that use Deye temperature offset: real_value = (raw - 1000) × scale
    temp_registers={100, 101},

    registers=[
        # RegisterDef(name, address, unit, scale, dtype, device_class, state_class, icon)
        RegisterDef("Battery SOC",   100, "%",  1,    "uint16", "battery",     "measurement",      "mdi:battery"),
        RegisterDef("Grid Power",    200, "W",  1,    "int16",  "power",       "measurement",      "mdi:transmission-tower"),
        RegisterDef("PV1 Power",     300, "W",  1,    "uint16", "power",       "measurement",      "mdi:solar-power"),
        RegisterDef("PV2 Power",     301, "W",  1,    "uint16", "power",       "measurement",      "mdi:solar-power"),
        RegisterDef("Today Import",  400, "kWh",0.1,  "uint16", "energy",      "total_increasing", "mdi:transmission-tower-import"),
        # ... remaining registers
    ],

    # Derived sensors computed from other registers (no Modbus address of their own)
    computed_registers=[
        ComputedRegisterDef(
            name="PV Total Power",
            unit="W",
            device_class="power",
            state_class="measurement",
            icon="mdi:solar-power",
            sources=["PV1 Power", "PV2 Power"],  # RegisterDef names to sum
        ),
    ],

    # read_blocks is OPTIONAL.
    # If omitted, blocks are auto-computed by grouping addresses with a gap <= 5.
    # Define explicitly for fine-grained control over Modbus reads
    # (useful when there are large address gaps between register groups).
    read_blocks=[
        (100, 2),   # Battery SOC + next
        (200, 1),   # Grid Power
        (300, 2),   # PV1 + PV2 Power
        (400, 1),   # Today Import
    ],
)
```

### Step 2 — Register in `inverters/__init__.py`

```python
from .brand_model import INVERTER as _BRAND_MODEL

_ALL: list[InverterDef] = [
    _DEYE_SUN8K_SG05LP3,
    _BRAND_MODEL,   # ← add here
]
```

The new model will appear automatically in the HA configuration dropdown.

### Type reference

#### `RegisterDef` — Modbus holding register

| Field | Type | Description |
|---|---|---|
| `name` | `str` | Sensor name (e.g. `"Battery SOC"`) |
| `address` | `int` | Holding register address |
| `unit` | `str` | Unit of measurement (`"W"`, `"V"`, `"A"`, `"%"`, `"°C"`, `"kWh"`, `"Hz"`, `""`) |
| `scale` | `float` | Multiplier applied to the raw value (e.g. `0.1` divides by 10) |
| `dtype` | `str` | `"uint16"` (unsigned) or `"int16"` (signed — for power and current values that can be negative) |
| `device_class` | `str\|None` | HA device class: `"voltage"`, `"current"`, `"power"`, `"energy"`, `"battery"`, `"temperature"`, `"frequency"`, or `None` |
| `state_class` | `str\|None` | `"measurement"` for instantaneous values, `"total_increasing"` for energy counters, or `None` |
| `icon` | `str` | MDI icon (e.g. `"mdi:solar-power"`) |

#### `ComputedRegisterDef` — derived sensor

| Field | Type | Description |
|---|---|---|
| `name` | `str` | Sensor name |
| `unit` | `str` | Unit of measurement |
| `device_class` | `str\|None` | HA device class |
| `state_class` | `str\|None` | HA state class |
| `icon` | `str` | MDI icon |
| `sources` | `list[str]` | Names of `RegisterDef` entries to sum (`None` values are ignored) |

#### Deye temperature offset

Some Deye inverter registers encode temperature with an offset of 1000:

```
real_value = (raw - 1000) × scale
```

Example: raw `1250` with scale `0.1` → `(1250 - 1000) × 0.1 = 25.0 °C`

Add the affected addresses to the `temp_registers={...}` field of `InverterDef`.

### Tips for mapping registers

1. Get the Modbus manual for your inverter (usually available on the manufacturer's website or community forums)
2. Look for the "Holding Registers" table (function code 0x03)
3. Check whether values are signed or unsigned — power and current values that can be negative are typically `int16`
4. Use a Modbus client (e.g. [ModbusPoll](https://www.modbustools.com/modbus_poll.html) or [QModMaster](https://sourceforge.net/projects/qmodmaster/)) to verify values against the live inverter before writing the definition

### Submitting a PR

1. Fork the repository
2. Create a branch: `git checkout -b inverter/brand-model`
3. Add the file in `inverters/` and register it in `inverters/__init__.py`
4. Test with your hardware and confirm the values make sense
5. Open a Pull Request including:
   - Exact inverter model (and any compatible variants)
   - Reference to the Modbus manual used
   - Screenshot or log of live readings for validation

---

## Architecture

```
custom_components/deye_modbus/
├── inverter_def.py          # base types: RegisterDef, ComputedRegisterDef, InverterDef
├── inverters/
│   ├── __init__.py          # registry of all supported models
│   └── deye_sun8k_sg05lp3.py  # Deye SUN-xK-SG05LP3-EU-SM2 definition
├── coordinator.py           # DataUpdateCoordinator — Modbus TCP polling
├── config_flow.py           # config flow + options flow (HA configuration UI)
├── sensor.py                # SensorEntity implementations
├── const.py                 # constants
└── __init__.py              # config entry setup / unload
```

### Read cycle

1. The coordinator opens a fresh TCP connection each polling cycle
2. Reads registers in **contiguous blocks** (fewer Modbus TCP transactions = less load on the RS485 bridge)
3. Waits 300 ms between blocks to avoid saturating the Waveshare adapter
4. Computes derived sensors (`ComputedRegisterDef`) after all reads are complete
5. Closes the TCP connection
6. HA updates all sensor states with the new values

---

## License

MIT
