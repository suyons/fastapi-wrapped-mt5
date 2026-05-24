# FastAPI Wrapped MT5

A FastAPI wrapper around the MetaTrader 5 (MT5) trading platform that exposes its full Python API as a REST service. This lets you run MT5 on a Windows machine and connect to it from any OS over HTTP.

## Quick start

```bash
# Git Bash / Linux
bash start.sh

# PowerShell (Windows) — with hot-reload on file changes
./start.ps1
```

The server starts on `http://0.0.0.0:8000`. Interactive API docs available at `http://localhost:8000/docs`.

> **Important**: call `POST /initialize` before any other endpoint to establish the MT5 connection.

---

## API reference with examples

All examples assume the server is at `http://localhost:8000`. Replace with your actual host/IP.

### Connection

#### POST /initialize

Establish a connection with the MT5 terminal.

```sh
curl -X POST 'http://localhost:8000/initialize' \
  -H 'accept: application/json'
```

```json
{"status": "success"}
```

#### POST /login

Log in to a trading account.

```sh
curl -X POST 'http://localhost:8000/login' \
  -H 'Content-Type: application/json' \
  -d '{"account": 12345678, "password": "your_password", "server": "BrokerName-Demo"}'
```

```json
{"status": "success"}
```

#### POST /shutdown

Close the MT5 terminal connection.

```sh
curl -X POST 'http://localhost:8000/shutdown' \
  -H 'accept: application/json'
```

```json
{"status": "success"}
```

---

### Info

#### GET /version

Return the MT5 terminal version.

```sh
curl 'http://localhost:8000/version'
```

```json
{"version": [500, 5833, "25 Apr 2026"]}
```

#### GET /last_error

Return the last error code and message.

```sh
curl 'http://localhost:8000/last_error'
```

```json
{"last_error": [1, "Success"]}
```

#### GET /account_info

Get current trading account information.

```sh
curl 'http://localhost:8000/account_info'
```

```json
{
  "status": "success",
  "info": {
    "login": 12345678,
    "trade_mode": 0,
    "leverage": 500,
    "limit_orders": 0,
    "margin_so_mode": 0,
    "trade_allowed": true,
    "trade_expert": true,
    "margin_mode": 2,
    "currency_digits": 2,
    "fifo_close": false,
    "balance": 99999.99,
    "credit": 0.0,
    "profit": 0.0,
    "equity": 99999.99,
    "margin": 0.0,
    "margin_free": 99999.99,
    "margin_level": 0.0,
    "margin_so_call": 100.0,
    "margin_so_so": 50.0,
    "margin_initial": 0.0,
    "margin_maintenance": 0.0,
    "assets": 0.0,
    "liabilities": 0.0,
    "commission_blocked": 0.0,
    "name": "Demo Account",
    "server": "BrokerName-Demo",
    "currency": "USD",
    "company": "Broker Corp."
  }
}
```

#### GET /terminal_info

Get status and parameters of the connected MT5 terminal.

```sh
curl 'http://localhost:8000/terminal_info'
```

```json
{
  "status": "success",
  "info": {
    "community_account": false,
    "community_connection": false,
    "connected": true,
    "dlls_allowed": false,
    "trade_allowed": true,
    "tradeapi_disabled": false,
    "email_enabled": false,
    "ftp_enabled": false,
    "notifications_enabled": false,
    "mqid": false,
    "build": 5833,
    "maxbars": 100000,
    "codepage": 0,
    "ping_last": 15,
    "community_balance": 0.0,
    "retransmission": 0.0,
    "company": "MetaQuotes Software Corp.",
    "name": "MetaTrader 5",
    "language": "English",
    "path": "C:\\Program Files\\MetaTrader 5",
    "data_path": "C:\\Users\\user\\AppData\\Roaming\\MetaQuotes\\Terminal\\...",
    "commondata_path": "C:\\Users\\user\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common"
  }
}
```

---

### Symbols

#### GET /symbols_total

Get the total number of available financial instruments.

```sh
curl 'http://localhost:8000/symbols_total'
```

```json
{"total": 967}
```

#### GET /symbols_get

Get all symbols, optionally filtered by group pattern (e.g. `*XAU*`).

```sh
curl 'http://localhost:8000/symbols_get?group=*XAU*'
```

```json
{
  "symbols": [
    {
      "name": "XAUUSD.r",
      "description": "Gold vs US Dollar",
      "digits": 2,
      "spread": 72,
      "trade_contract_size": 100.0,
      "volume_min": 0.01,
      "volume_max": 20.0,
      "bid": 4509.26,
      "ask": 4509.98
    }
  ]
}
```

#### GET /symbol_info/{symbol}

Get full data for a specific symbol.

```sh
curl 'http://localhost:8000/symbol_info/XAUUSD.r'
```

```json
{
  "status": "success",
  "info": {
    "name": "XAUUSD.r",
    "digits": 2,
    "spread": 72,
    "point": 0.01,
    "trade_contract_size": 100.0,
    "volume_min": 0.01,
    "volume_max": 20.0,
    "swap_long": -71.5,
    "swap_short": 32.5,
    "bid": 4509.26,
    "ask": 4509.98
  }
}
```

#### GET /symbol_info_tick/{symbol}

Get the latest tick for a symbol.

```sh
curl 'http://localhost:8000/symbol_info_tick/XAUUSD.r'
```

```json
{
  "status": "success",
  "tick": {
    "time": 1764343500,
    "bid": 4170.64,
    "ask": 4170.91,
    "last": 0.0,
    "volume": 0,
    "time_msc": 1764343500788,
    "flags": 6,
    "volume_real": 0.0
  }
}
```

#### POST /symbol_select/{symbol}

Add or remove a symbol from the MarketWatch window.

```sh
curl -X POST 'http://localhost:8000/symbol_select/XAUUSD.r?enable=true'
```

```json
{"status": "success"}
```

---

### Market Data

All timeframe values match the MT5 integer constants:

| Timeframe | Value |
|-----------|-------|
| M1        | 1     |
| M5        | 5     |
| M15       | 15    |
| H1        | 16385 |
| H4        | 16388 |
| D1        | 32769 |

#### GET /copy_rates_from_pos/{symbol}

Get bars starting from a position index. `start_pos=0` is the current forming bar; `start_pos=1` is the latest completed bar.

```sh
curl 'http://localhost:8000/copy_rates_from_pos/XAUUSD.r?timeframe=5&start_pos=0&count=3'
```

```json
{
  "status": "success",
  "rates": [
    {
      "time": 1764343500,
      "open": 4170.64,
      "high": 4171.07,
      "low": 4168.94,
      "close": 4170.60,
      "tick_volume": 158,
      "spread": 2,
      "real_volume": 0
    },
    {
      "time": 1764343800,
      "open": 4169.16,
      "high": 4177.21,
      "low": 4168.94,
      "close": 4176.77,
      "tick_volume": 291,
      "spread": 7,
      "real_volume": 0
    },
    {
      "time": 1764344100,
      "open": 4176.22,
      "high": 4178.62,
      "low": 4176.17,
      "close": 4176.62,
      "tick_volume": 83,
      "spread": 7,
      "real_volume": 0
    }
  ]
}
```

#### GET /copy_rates_from/{symbol}

Get `count` bars starting from a specified date (ISO 8601).

```sh
curl 'http://localhost:8000/copy_rates_from/XAUUSD.r?timeframe=5&date_from=2025-05-01T00:00:00&count=3'
```

Response format is the same as `copy_rates_from_pos`.

#### GET /copy_rates_range/{symbol}

Get all bars within a date range.

```sh
curl 'http://localhost:8000/copy_rates_range/XAUUSD.r?timeframe=5&date_from=2025-05-01T07:00:00&date_to=2025-05-01T08:00:00'
```

Response format is the same as `copy_rates_from_pos`.

#### GET /copy_ticks_from/{symbol}

Get `count` ticks starting from a specified date. `flags=1` returns bid/ask ticks.

```sh
curl 'http://localhost:8000/copy_ticks_from/XAUUSD.r?date_from=2025-05-01T07:00:00&count=3&flags=1'
```

```json
{
  "status": "success",
  "ticks": [
    {
      "time": 1746061260,
      "bid": 3288.44,
      "ask": 3288.56,
      "last": 0.0,
      "volume": 0,
      "time_msc": 1746061260596,
      "flags": 134,
      "volume_real": 0.0
    }
  ]
}
```

#### GET /copy_ticks_range/{symbol}

Get all ticks within a date range.

```sh
curl 'http://localhost:8000/copy_ticks_range/XAUUSD.r?date_from=2025-12-10T01:00:00&date_to=2025-12-10T01:05:00&flags=1'
```

Response format is the same as `copy_ticks_from`.

#### POST /market_book_add/{symbol}

Subscribe to Market Depth change events. Not supported by all brokers.

```sh
curl -X POST 'http://localhost:8000/market_book_add/XAUUSD.r'
```

#### GET /market_book_get/{symbol}

Get current Market Depth entries. Requires a prior `market_book_add` call.

```sh
curl 'http://localhost:8000/market_book_get/XAUUSD.r'
```

#### POST /market_book_release/{symbol}

Cancel Market Depth subscription.

```sh
curl -X POST 'http://localhost:8000/market_book_release/XAUUSD.r'
```

---

### Orders

#### GET /orders_total

Get the number of currently active (pending) orders.

```sh
curl 'http://localhost:8000/orders_total'
```

```json
{"total": 0}
```

#### GET /orders_get

Get active orders, optionally filtered by `symbol` or `ticket`.

```sh
curl 'http://localhost:8000/orders_get?symbol=XAUUSD.r'
```

```json
{"status": "success", "orders": []}
```

#### POST /order_calc_margin

Calculate the margin required for a trade. Provide `type` (0=BUY, 1=SELL), `symbol`, `volume`, and `price`.

```sh
curl -X POST 'http://localhost:8000/order_calc_margin' \
  -H 'Content-Type: application/json' \
  -d '{"symbol": "XAUUSD.r", "volume": 0.01, "type": 0, "price": 4500.0}'
```

```json
{"status": "success", "margin": 9.0}
```

#### POST /order_calc_profit

Calculate expected profit. Use `price` for the open price and `tp` for the target close price.

```sh
curl -X POST 'http://localhost:8000/order_calc_profit' \
  -H 'Content-Type: application/json' \
  -d '{"symbol": "XAUUSD.r", "volume": 0.01, "type": 0, "price": 4500.0, "tp": 4510.0}'
```

```json
{"status": "success", "profit": 10.0}
```

#### POST /order_check

Check if there are sufficient funds for a trade without sending it.

```sh
curl -X POST 'http://localhost:8000/order_check' \
  -H 'Content-Type: application/json' \
  -d '{
    "symbol": "XAUUSD.r",
    "volume": 0.01,
    "type": 0,
    "price": 4509.98,
    "type_filling": 1
  }'
```

```json
{
  "status": "success",
  "result": {
    "retcode": 0,
    "balance": 99999.99,
    "equity": 99999.99,
    "profit": 0.0,
    "margin": 9.0,
    "margin_free": 99990.99,
    "margin_level": 1111111.0,
    "comment": "Done",
    "request": [1, 0, 0, "XAUUSD.r", 0.01, 4509.98, 0.0, 0.0, 0.0, 0, 0, 1, 0, 0, "", 0, 0]
  }
}
```

#### POST /order_send — Open a market order

Place a market buy or sell order. `type`: 0=BUY, 1=SELL. `type_filling`: 0=FOK, 1=IOC, 2=RETURN.

```sh
curl -X POST 'http://localhost:8000/order_send' \
  -H 'Content-Type: application/json' \
  -d '{
    "symbol": "XAUUSD.r",
    "volume": 0.01,
    "type": 0,
    "sl": 4490.0,
    "tp": 4530.0,
    "deviation": 10,
    "magic": 0,
    "comment": "api_order",
    "type_time": 0,
    "type_filling": 1
  }'
```

```json
{
  "status": "success",
  "result": {
    "retcode": 10009,
    "deal": 175962659,
    "order": 242847567,
    "volume": 0.01,
    "price": 4172.71,
    "bid": 0.0,
    "ask": 0.0,
    "comment": "Request executed",
    "request_id": 698305145,
    "retcode_external": 0,
    "request": [1, 0, 0, "XAUUSD.r", 0.01, 0.0, 0.0, 4490.0, 4530.0, 10, 0, 1, 0, 0, "api_order", 0, 0]
  }
}
```

#### POST /order_send — Modify SL/TP of an open position

Provide `position` (ticket), `symbol`, `sl`, and `tp`.

```sh
curl -X POST 'http://localhost:8000/order_send' \
  -H 'Content-Type: application/json' \
  -d '{
    "symbol": "XAUUSD.r",
    "volume": 0.01,
    "sl": 4100.0,
    "tp": 4500.0,
    "position": 242847567
  }'
```

```json
{
  "status": "success",
  "result": {
    "retcode": 10009,
    "deal": 0,
    "order": 0,
    "volume": 0.0,
    "price": 0.0,
    "comment": "Request executed",
    "request_id": 698305409,
    "retcode_external": 0,
    "request": [6, 0, 0, "XAUUSD.r", 0.01, 4172.71, 0.0, 4100.0, 4500.0, 0, 0, 0, 0, 0, "", 242847567, 0]
  }
}
```

#### POST /order_send — Close an open position

Provide `position` (ticket), `symbol`, and `volume`. Leave `sl`/`tp` at 0.

```sh
curl -X POST 'http://localhost:8000/order_send' \
  -H 'Content-Type: application/json' \
  -d '{
    "symbol": "XAUUSD.r",
    "volume": 0.01,
    "position": 242847567,
    "sl": 0,
    "tp": 0,
    "type_time": 0,
    "type_filling": 1
  }'
```

```json
{
  "status": "success",
  "result": {
    "retcode": 10009,
    "deal": 178779133,
    "order": 246783180,
    "volume": 0.01,
    "price": 4181.57,
    "comment": "Request executed",
    "request_id": 698305778,
    "retcode_external": 0,
    "request": [1, 0, 0, "XAUUSD.r", 0.01, 4181.33, 0.0, 0.0, 0.0, 0, 1, 1, 0, 0, "", 242847567, 0]
  }
}
```

---

### Positions

#### GET /positions_total

Get the number of open positions.

```sh
curl 'http://localhost:8000/positions_total'
```

```json
{"total": 6}
```

#### GET /positions_get

Get open positions, optionally filtered by `symbol` or `ticket`.

```sh
curl 'http://localhost:8000/positions_get?symbol=XAUUSD.r'
```

```json
{
  "status": "success",
  "positions": [
    {
      "ticket": 242847567,
      "time": 1764814516,
      "time_msc": 1764814516954,
      "time_update": 1764814516,
      "time_update_msc": 1764814516954,
      "type": 1,
      "magic": 0,
      "identifier": 242847567,
      "reason": 3,
      "volume": 0.01,
      "price_open": 4207.76,
      "sl": 4100.0,
      "tp": 4500.0,
      "price_current": 4207.68,
      "swap": 0.0,
      "profit": 0.08,
      "symbol": "XAUUSD.r",
      "comment": "api_order",
      "external_id": ""
    }
  ]
}
```

---

### History

#### GET /history_orders_total

Get the count of historical orders in a date range.

```sh
curl 'http://localhost:8000/history_orders_total?date_from=2025-05-01T00:00:00&date_to=2025-05-31T23:59:59'
```

```json
{"total": 42}
```

#### GET /history_orders_get

Get historical orders. Filter by `group` pattern, or look up a single order by `ticket` or `position`.

```sh
# By date range
curl 'http://localhost:8000/history_orders_get?date_from=2025-05-01T00:00:00&date_to=2025-05-31T23:59:59'

# By ticket (date params still required but ignored when ticket is set)
curl 'http://localhost:8000/history_orders_get?date_from=2025-01-01T00:00:00&date_to=2026-01-01T00:00:00&ticket=242847567'
```

```json
{
  "status": "success",
  "orders": [
    {
      "ticket": 242847567,
      "time_setup": 1764814516,
      "time_setup_msc": 1764814516954,
      "time_done": 1764814516,
      "type": 1,
      "type_filling": 1,
      "state": 4,
      "volume_initial": 0.01,
      "volume_current": 0.0,
      "price_open": 0.0,
      "sl": 4100.0,
      "tp": 4500.0,
      "price_current": 4207.76,
      "symbol": "XAUUSD.r",
      "comment": "api_order"
    }
  ]
}
```

#### GET /history_deals_total

Get the count of historical deals in a date range.

```sh
curl 'http://localhost:8000/history_deals_total?date_from=2025-05-01T00:00:00&date_to=2025-05-31T23:59:59'
```

```json
{"total": 84}
```

#### GET /history_deals_get

Get historical deals. Filter by `group` pattern, or look up by `ticket` (deal ticket) or `position` (position ID).

```sh
# By date range
curl 'http://localhost:8000/history_deals_get?date_from=2025-05-01T00:00:00&date_to=2025-05-31T23:59:59'

# By position ID — useful for per-trade PnL lookup
curl 'http://localhost:8000/history_deals_get?date_from=2025-01-01T00:00:00&date_to=2026-01-01T00:00:00&position=242847567'
```

```json
{
  "status": "success",
  "deals": [
    {
      "ticket": 175962659,
      "order": 242847567,
      "time": 1764814516,
      "time_msc": 1764814516954,
      "type": 1,
      "entry": 0,
      "magic": 0,
      "position_id": 242847567,
      "reason": 3,
      "volume": 0.01,
      "price": 4172.71,
      "commission": -0.48,
      "swap": 0.0,
      "profit": 0.0,
      "fee": 0.0,
      "symbol": "XAUUSD.r",
      "comment": "api_order",
      "external_id": ""
    }
  ]
}
```

---

## Order type reference

**type** (ORDER_TYPE)

| Value | Name                       |
|-------|----------------------------|
| 0     | ORDER_TYPE_BUY             |
| 1     | ORDER_TYPE_SELL            |
| 2     | ORDER_TYPE_BUY_LIMIT       |
| 3     | ORDER_TYPE_SELL_LIMIT      |
| 4     | ORDER_TYPE_BUY_STOP        |
| 5     | ORDER_TYPE_SELL_STOP       |
| 6     | ORDER_TYPE_BUY_STOP_LIMIT  |
| 7     | ORDER_TYPE_SELL_STOP_LIMIT |
| 8     | ORDER_TYPE_CLOSE_BY        |

**type_filling** (ORDER_FILLING)

| Value | Name                  |
|-------|-----------------------|
| 0     | ORDER_FILLING_FOK     |
| 1     | ORDER_FILLING_IOC     |
| 2     | ORDER_FILLING_RETURN  |

**type_time** (ORDER_TIME)

| Value | Name                      |
|-------|---------------------------|
| 0     | ORDER_TIME_GTC            |
| 1     | ORDER_TIME_DAY            |
| 2     | ORDER_TIME_SPECIFIED      |
| 3     | ORDER_TIME_SPECIFIED_DAY  |
