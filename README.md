# Deye Modbus — Home Assistant Custom Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/v/release/leonelfaugusto/deye-modbus-tcp)](https://github.com/leonelfaugusto/deye-modbus-tcp/releases)
[![HA version](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-blue)](https://www.home-assistant.io/)

Custom component para Home Assistant que lê dados de inversores solares via Modbus TCP, usando um conversor RS485-to-WiFi (Waveshare ou compatível) como bridge.

---

## Inversores suportados

| Modelo | Ficheiro | Fases | Strings PV |
|---|---|---|---|
| Deye SUN-xK-SG05LP3-EU-SM2 | `deye_sun8k_sg05lp3` | 3 | 4 |

> Compatível com as variantes SUN-5K, SUN-6K, SUN-8K, SUN-10K da série SG05LP3 que partilham o mesmo mapa de registos Modbus RTU V105.4.

Queres adicionar o teu inversor? Ver a secção **[Contribuir — Adicionar um novo inversor](#contribuir--adicionar-um-novo-inversor)**.

---

## Hardware testado

| Componente | Modelo |
|---|---|
| Inversor | Deye SUN-8K-SG05LP3-EU-SM2 |
| Conversor RS485 | Waveshare RS485 to WiFi/ETH |

### Requisitos de hardware

- Waveshare configurado em modo **Modbus TCP ⟺ Modbus RTU** (não Transparent)
- Inversor com **Modbus SN = 01** (em Advanced Function no display)
- Baud rate: **9600 bps, 8N1** — igual no Waveshare e no inversor
- Não usar o modo Transparent do Waveshare — o framing TCP/RTU é diferente

---

## Instalação via HACS

1. Em HACS → Integrations → ⋮ → **Custom repositories**
2. Adicionar `https://github.com/leonelfaugusto/deye-modbus-tcp`, categoria: **Integration**
3. Instalar **Deye Modbus**
4. Reiniciar o Home Assistant
5. Ir a **Definições → Integrações → Adicionar integração → Deye Modbus**

## Instalação manual

Copiar a pasta `custom_components/deye_modbus/` para `<config>/custom_components/` e reiniciar o HA.

---

## Configuração

| Campo | Padrão | Descrição |
|---|---|---|
| Modelo do inversor | — | Seleccionar da lista de modelos suportados |
| Host (IP) | `10.10.20.102` | IP do conversor Waveshare |
| Porta TCP | `8899` | Porta TCP do Waveshare |
| Modbus Slave ID | `1` | Slave ID configurado no inversor |
| Intervalo de polling | `10` | Segundos entre leituras (mín. 5s) |

### Alterar definições após configuração

Vai a **Definições → Integrações → Deye Modbus → Configurar**. Todas as definições podem ser alteradas sem perder o histórico dos sensores.

---

## Sensores criados

O componente cria um único dispositivo com todos os sensores agrupados.

### Deye SUN-xK-SG05LP3-EU-SM2 (48 sensores)

| Grupo | Sensores |
|---|---|
| Estado | Run State |
| Grid | L1/L2/L3 Voltage · L1/L2/L3 Power · Total Power · Frequency |
| PV | PV1–PV4 Power · PV1/PV2 Voltage · PV1/PV2 Current · **PV Total Power** ¹ |
| Inversor | L1/L2/L3 Power · Total Power · L1/L2/L3 Voltage |
| Load | L1/L2/L3 Power · Total Power |
| Bateria | SOC · Voltage · Current · Power · Temperature |
| Temperatura | DC Transformer Temp · Heat Sink Temp |
| Energia diária | Generation · Grid Buy · Grid Sell · Load · Battery Charge · Battery Discharge |
| CT externo | CT1/CT2/CT3 Current · CT1/CT2/CT3 Power · Total Power |

¹ **PV Total Power** é calculado automaticamente como a soma dos strings PV activos (ignora strings não ligados).

### Convenções de sinal

| Sensor | Valor positivo | Valor negativo |
|---|---|---|
| Grid Power | Importação da rede | Exportação para a rede |
| Battery Power | Descarga da bateria | Carga da bateria |
| Battery Current | Descarga | Carga |

---

## Energy Dashboard

Os seguintes sensores são compatíveis com o Energy Dashboard do Home Assistant (`state_class: total_increasing`):

- `Today Generation` → Produção solar
- `Today Grid Buy` → Consumo da rede
- `Today Grid Sell` → Exportação para a rede
- `Today Load` → Consumo total da casa
- `Today Battery Charge` → Energia de carga da bateria
- `Today Battery Discharge` → Energia de descarga da bateria

---

## Contribuir — Adicionar um novo inversor

A integração foi desenhada para ser facilmente extensível. Cada modelo de inversor é definido num ficheiro Python independente em `custom_components/deye_modbus/inverters/`.

### Passo 1 — Criar o ficheiro de definição

Cria `custom_components/deye_modbus/inverters/<chave_do_modelo>.py`:

```python
"""Descrição do inversor e referências ao manual Modbus."""
from __future__ import annotations

from ..inverter_def import ComputedRegisterDef, InverterDef, RegisterDef

INVERTER = InverterDef(
    key="fabricante_modelo",           # identificador único, sem espaços
    name="Fabricante Modelo-XYZ",      # nome no dropdown de configuração
    manufacturer="Fabricante",
    model="Modelo-XYZ",

    # Registos com offset de temperatura: valor_real = (raw - 1000) × scale
    temp_registers={100, 101},

    registers=[
        # RegisterDef(nome, endereço, unidade, scale, dtype, device_class, state_class, icon)
        RegisterDef("Battery SOC",   100, "%",  1,    "uint16", "battery",     "measurement",      "mdi:battery"),
        RegisterDef("Grid Power",    200, "W",  1,    "int16",  "power",       "measurement",      "mdi:transmission-tower"),
        RegisterDef("PV1 Power",     300, "W",  1,    "uint16", "power",       "measurement",      "mdi:solar-power"),
        RegisterDef("PV2 Power",     301, "W",  1,    "uint16", "power",       "measurement",      "mdi:solar-power"),
        RegisterDef("Today Import",  400, "kWh",0.1,  "uint16", "energy",      "total_increasing", "mdi:transmission-tower-import"),
        # ... restantes registos
    ],

    # Sensores calculados a partir de outros registos (sem endereço Modbus)
    computed_registers=[
        ComputedRegisterDef(
            name="PV Total Power",
            unit="W",
            device_class="power",
            state_class="measurement",
            icon="mdi:solar-power",
            sources=["PV1 Power", "PV2 Power"],  # nomes de RegisterDef a somar
        ),
    ],

    # read_blocks é OPCIONAL.
    # Se omitido, é calculado automaticamente agrupando endereços com gap ≤ 5.
    # Define-o explicitamente para controlo fino sobre as leituras Modbus
    # (útil quando há gaps grandes entre grupos de registos).
    read_blocks=[
        (100, 2),   # Battery SOC + outro
        (200, 1),   # Grid Power
        (300, 2),   # PV1 + PV2 Power
        (400, 1),   # Today Import
    ],
)
```

### Passo 2 — Registar em `inverters/__init__.py`

```python
from .fabricante_modelo import INVERTER as _FABRICANTE_MODELO

_ALL: list[InverterDef] = [
    _DEYE_SUN8K_SG05LP3,
    _FABRICANTE_MODELO,   # ← adicionar aqui
]
```

O novo modelo aparece automaticamente no dropdown de configuração do HA.

### Referência de tipos

#### `RegisterDef` — registo Modbus

| Campo | Tipo | Descrição |
|---|---|---|
| `name` | `str` | Nome do sensor (ex: `"Battery SOC"`) |
| `address` | `int` | Endereço do holding register |
| `unit` | `str` | Unidade (`"W"`, `"V"`, `"A"`, `"%"`, `"°C"`, `"kWh"`, `"Hz"`, `""`) |
| `scale` | `float` | Multiplicador aplicado ao valor raw (ex: `0.1` para divisão por 10) |
| `dtype` | `str` | `"uint16"` (sem sinal) ou `"int16"` (com sinal, para potências e correntes que podem ser negativas) |
| `device_class` | `str\|None` | Classe HA: `"voltage"`, `"current"`, `"power"`, `"energy"`, `"battery"`, `"temperature"`, `"frequency"`, ou `None` |
| `state_class` | `str\|None` | `"measurement"` para valores instantâneos, `"total_increasing"` para contadores de energia, ou `None` |
| `icon` | `str` | Ícone MDI (ex: `"mdi:solar-power"`) |

#### `ComputedRegisterDef` — sensor derivado

| Campo | Tipo | Descrição |
|---|---|---|
| `name` | `str` | Nome do sensor |
| `unit` | `str` | Unidade |
| `device_class` | `str\|None` | Classe HA |
| `state_class` | `str\|None` | Classe de estado |
| `icon` | `str` | Ícone MDI |
| `sources` | `list[str]` | Nomes de `RegisterDef` a somar (valores `None` são ignorados) |

#### Temperatura com offset Deye

Alguns inversores Deye codificam a temperatura com offset de 1000:

```
valor_real = (raw - 1000) × scale
```

Exemplo: raw `1250` com scale `0.1` → `(1250 - 1000) × 0.1 = 25.0 °C`

Adiciona os endereços afectados ao campo `temp_registers={...}` do `InverterDef`.

### Dicas para mapear registos

1. Obtém o manual Modbus do teu inversor (geralmente disponível no site do fabricante ou em grupos de utilizadores)
2. Procura a tabela de "Holding Registers" (function code 0x03)
3. Verifica se os valores signed/unsigned correspondem ao que lês — potências e correntes que podem ser negativas são geralmente `int16`
4. Usa um cliente Modbus (ex: [ModbusPoll](https://www.modbustools.com/modbus_poll.html) ou [QModMaster](https://sourceforge.net/projects/qmodmaster/)) para validar os valores antes de criar a definição

### Submeter um PR

1. Fork do repositório
2. Cria um branch: `git checkout -b inverter/fabricante-modelo`
3. Adiciona o ficheiro em `inverters/` e regista em `inverters/__init__.py`
4. Testa com o teu hardware e confirma que os valores fazem sentido
5. Abre um Pull Request com:
   - Modelo exacto do inversor (incluindo variantes compatíveis)
   - Referência ao manual Modbus utilizado
   - Printscreen ou log de valores lidos para validação

---

## Arquitectura

```
custom_components/deye_modbus/
├── inverter_def.py          # tipos base: RegisterDef, ComputedRegisterDef, InverterDef
├── inverters/
│   ├── __init__.py          # registo de todos os modelos suportados
│   └── deye_sun8k_sg05lp3.py  # definição do Deye SUN-xK-SG05LP3-EU-SM2
├── coordinator.py           # DataUpdateCoordinator — leitura Modbus TCP
├── config_flow.py           # config flow + options flow (UI de configuração)
├── sensor.py                # entidades SensorEntity
├── const.py                 # constantes
└── __init__.py              # setup/unload da config entry
```

### Fluxo de leitura

1. O coordinator abre uma ligação TCP nova em cada ciclo de polling
2. Lê os registos em **blocos consecutivos** (menos transações Modbus TCP = menos pressão sobre o bridge RS485)
3. Aguarda 300ms entre blocos para não saturar o Waveshare
4. Calcula os sensores derivados (`ComputedRegisterDef`) após a leitura
5. Fecha a ligação TCP
6. O HA actualiza os estados dos sensores com os novos valores

---

## Licença

MIT
