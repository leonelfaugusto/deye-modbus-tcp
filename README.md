# Deye Modbus — Home Assistant Custom Integration

Custom component para Home Assistant que lê dados de inversores solares Deye trifásicos via Modbus TCP, usando um conversor Waveshare RS485-to-WiFi como bridge.

## Hardware suportado

| Componente | Modelo |
|---|---|
| Inversor | Deye SUN-8K-SG05LP3-EU-SM2 (e variantes trifásicas) |
| Conversor | Waveshare RS485 to WiFi/ETH |

## Requisitos

- Home Assistant 2024.1.0+
- pymodbus 3.7.4
- Waveshare configurado em modo **Modbus TCP ⟺ Modbus RTU** (não Transparent)
- Deye com **Modbus SN = 01** (Advanced Function no display)
- Baud rate: **9600 bps, 8N1** — igual no Waveshare e no Deye

## Instalação via HACS

1. Em HACS → Integrations → ⋮ → Custom repositories
2. Adicionar URL deste repositório, categoria: **Integration**
3. Instalar **Deye Modbus**
4. Reiniciar o Home Assistant
5. Ir a **Definições → Integrações → Adicionar integração → Deye Modbus**

## Instalação manual

Copiar a pasta `custom_components/deye_modbus/` para `<config>/custom_components/` e reiniciar.

## Configuração

| Campo | Padrão | Descrição |
|---|---|---|
| Host | `10.10.20.102` | IP do Waveshare |
| Port | `8899` | Porta TCP |
| Slave ID | `1` | Modbus Slave ID do inversor |
| Scan interval | `10` | Intervalo de polling em segundos |

## Sensores criados (47)

O componente cria um único dispositivo **Deye Inverter** com os seguintes sensores:

### Estado
- Run State

### Grid (rede elétrica)
- Grid L1/L2/L3 Voltage, Grid L1/L2/L3 Power, Grid Total Power, Grid Frequency

### PV (solar)
- PV1/PV2/PV3/PV4 Power, PV1/PV2 Voltage, PV1/PV2 Current

### Inversor
- Inverter L1/L2/L3 Power, Inverter Total Power, Inverter L1/L2/L3 Voltage

### Load (consumo)
- Load L1/L2/L3 Power, Load Total Power

### Bateria
- Battery SOC, Voltage, Current, Power, Temperature

### Temperatura
- DC Transformer Temp, Heat Sink Temp

### Energia diária
- Today Generation, Today Grid Buy, Today Grid Sell, Today Load, Today Battery Charge, Today Battery Discharge

### CT externo (CT01 LoRa)
- External CT1/CT2/CT3 Current, External CT1/CT2/CT3 Power, External Total Power

## Convenções de sinal

- **Grid Power negativo** = exportação para a rede
- **Battery Power negativo** = bateria a carregar

## Energy Dashboard

Os sensores `Today Generation`, `Today Grid Buy`, `Today Grid Sell`, `Today Load`, `Today Battery Charge` e `Today Battery Discharge` são compatíveis com o Energy Dashboard do Home Assistant (`state_class: total_increasing`).
