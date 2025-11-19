from datetime import datetime
from enum import Enum

from fastapi import FastAPI
import MetaTrader5 as mt5
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class TimeFrame(Enum):
    TIMEFRAME_M1 = mt5.TIMEFRAME_M1
    TIMEFRAME_M2 = mt5.TIMEFRAME_M2
    TIMEFRAME_M3 = mt5.TIMEFRAME_M3
    TIMEFRAME_M4 = mt5.TIMEFRAME_M4
    TIMEFRAME_M5 = mt5.TIMEFRAME_M5
    TIMEFRAME_M6 = mt5.TIMEFRAME_M6
    TIMEFRAME_M10 = mt5.TIMEFRAME_M10
    TIMEFRAME_M12 = mt5.TIMEFRAME_M12
    TIMEFRAME_M15 = mt5.TIMEFRAME_M15
    TIMEFRAME_M20 = mt5.TIMEFRAME_M20
    TIMEFRAME_M30 = mt5.TIMEFRAME_M30
    TIMEFRAME_H1 = mt5.TIMEFRAME_H1
    TIMEFRAME_H2 = mt5.TIMEFRAME_H2
    TIMEFRAME_H3 = mt5.TIMEFRAME_H3
    TIMEFRAME_H4 = mt5.TIMEFRAME_H4
    TIMEFRAME_H6 = mt5.TIMEFRAME_H6
    TIMEFRAME_H8 = mt5.TIMEFRAME_H8
    TIMEFRAME_H12 = mt5.TIMEFRAME_H12
    TIMEFRAME_W1 = mt5.TIMEFRAME_W1
    TIMEFRAME_MN1 = mt5.TIMEFRAME_MN1


class OrderType(Enum):
    ORDER_TYPE_BUY = mt5.ORDER_TYPE_BUY
    ORDER_TYPE_SELL = mt5.ORDER_TYPE_SELL
    ORDER_TYPE_BUY_LIMIT = mt5.ORDER_TYPE_BUY_LIMIT
    ORDER_TYPE_SELL_LIMIT = mt5.ORDER_TYPE_SELL_LIMIT
    ORDER_TYPE_BUY_STOP = mt5.ORDER_TYPE_BUY_STOP
    ORDER_TYPE_SELL_STOP = mt5.ORDER_TYPE_SELL_STOP
    ORDER_TYPE_BUY_STOP_LIMIT = mt5.ORDER_TYPE_BUY_STOP_LIMIT
    ORDER_TYPE_SELL_STOP_LIMIT = mt5.ORDER_TYPE_SELL_STOP_LIMIT
    ORDER_TYPE_CLOSE_BY = mt5.ORDER_TYPE_CLOSE_BY


class OrderRequest(BaseModel):
    symbol: str
    volume: float
    type: OrderType
    price: float = 0
    sl: float = 0
    tp: float = 0
    deviation: int = 0
    magic: int = 0
    comment: str = ""
    type_time: int = 0
    type_filling: int = 0


class LoginRequest(BaseModel):
    account: int
    password: str
    server: str


@app.post("/initialize")
async def initialize():
    if not mt5.initialize():
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success"}


@app.post("/login")
async def login(login_request: LoginRequest):
    if not mt5.login(
        login_request.account,
        password=login_request.password,
        server=login_request.server,
    ):
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success"}


@app.post("/shutdown")
async def shutdown():
    mt5.shutdown()
    return {"status": "success"}


@app.get("/version")
async def version():
    return {"version": mt5.version()}


@app.get("/last_error")
async def last_error():
    return {"last_error": mt5.last_error()}


@app.get("/account_info")
async def account_info():
    info = mt5.account_info()
    if info is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "info": info._asdict()}


@app.get("/terminal_info")
async def terminal_info():
    info = mt5.terminal_info()
    if info is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "info": info._asdict()}


@app.get("/symbols_total")
async def symbols_total():
    return {"total": mt5.symbols_total()}


@app.get("/symbols_get")
async def symbols_get(group: str = None):
    if group:
        symbols = mt5.symbols_get(group)
    else:
        symbols = mt5.symbols_get()
    return {"symbols": [s._asdict() for s in symbols]}


@app.get("/symbol_info/{symbol}")
async def symbol_info(symbol: str):
    info = mt5.symbol_info(symbol)
    if info is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "info": info._asdict()}


@app.get("/symbol_info_tick/{symbol}")
async def symbol_info_tick(symbol: str):
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "tick": tick._asdict()}


@app.post("/symbol_select/{symbol}")
async def symbol_select(symbol: str, enable: bool):
    if not mt5.symbol_select(symbol, enable):
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success"}


@app.post("/market_book_add/{symbol}")
async def market_book_add(symbol: str):
    if not mt5.market_book_add(symbol):
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success"}


@app.get("/market_book_get/{symbol}")
async def market_book_get(symbol: str):
    book = mt5.market_book_get(symbol)
    if book is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "book": book}


@app.post("/market_book_release/{symbol}")
async def market_book_release(symbol: str):
    if not mt5.market_book_release(symbol):
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success"}


@app.get("/copy_rates_from/{symbol}")
async def copy_rates_from(
    symbol: str, timeframe: TimeFrame, date_from: datetime, count: int
):
    rates = mt5.copy_rates_from(symbol, timeframe.value, date_from, count)
    if rates is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "rates": rates}


@app.get("/copy_rates_from_pos/{symbol}")
async def copy_rates_from_pos(
    symbol: str, timeframe: TimeFrame, start_pos: int, count: int
):
    rates = mt5.copy_rates_from_pos(symbol, timeframe.value, start_pos, count)
    if rates is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "rates": rates}


@app.get("/copy_rates_range/{symbol}")
async def copy_rates_range(
    symbol: str, timeframe: TimeFrame, date_from: datetime, date_to: datetime
):
    rates = mt5.copy_rates_range(symbol, timeframe.value, date_from, date_to)
    if rates is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "rates": rates}


@app.get("/copy_ticks_from/{symbol}")
async def copy_ticks_from(symbol: str, date_from: datetime, count: int, flags: int):
    ticks = mt5.copy_ticks_from(symbol, date_from, count, flags)
    if ticks is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "ticks": ticks}


@app.get("/copy_ticks_range/{symbol}")
async def copy_ticks_range(
    symbol: str, date_from: datetime, date_to: datetime, flags: int
):
    ticks = mt5.copy_ticks_range(symbol, date_from, date_to, flags)
    if ticks is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "ticks": ticks}


@app.get("/orders_total")
async def orders_total():
    return {"total": mt5.orders_total()}


@app.get("/orders_get")
async def orders_get(symbol: str = None, ticket: int = None):
    if symbol:
        orders = mt5.orders_get(symbol=symbol)
    elif ticket:
        orders = mt5.orders_get(ticket=ticket)
    else:
        orders = mt5.orders_get()
    if orders is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "orders": [o._asdict() for o in orders]}


@app.post("/order_calc_margin")
async def order_calc_margin(order_request: OrderRequest):
    margin = mt5.order_calc_margin(
        order_request.type.value,
        order_request.symbol,
        order_request.volume,
        order_request.price,
    )
    if margin is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "margin": margin}


@app.post("/order_calc_profit")
async def order_calc_profit(order_request: OrderRequest):
    profit = mt5.order_calc_profit(
        order_request.type.value,
        order_request.symbol,
        order_request.volume,
        order_request.price,
        order_request.sl,
    )
    if profit is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "profit": profit}


@app.post("/order_check")
async def order_check(order_request: OrderRequest):
    result = mt5.order_check(order_request.dict())
    if result is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "result": result._asdict()}


@app.post("/order_send")
async def order_send(order_request: OrderRequest):
    result = mt5.order_send(order_request.dict())
    if result is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "result": result._asdict()}


@app.get("/positions_total")
async def positions_total():
    return {"total": mt5.positions_total()}


@app.get("/positions_get")
async def positions_get(symbol: str = None, ticket: int = None):
    if symbol:
        positions = mt5.positions_get(symbol=symbol)
    elif ticket:
        positions = mt5.positions_get(ticket=ticket)
    else:
        positions = mt5.positions_get()
    if positions is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "positions": [p._asdict() for p in positions]}


@app.get("/history_orders_total")
async def history_orders_total(date_from: datetime, date_to: datetime):
    total = mt5.history_orders_total(date_from, date_to)
    return {"total": total}


@app.get("/history_orders_get")
async def history_orders_get(date_from: datetime, date_to: datetime, group: str = None):
    if group:
        orders = mt5.history_orders_get(date_from, date_to, group=group)
    else:
        orders = mt5.history_orders_get(date_from, date_to)
    if orders is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "orders": [o._asdict() for o in orders]}


@app.get("/history_deals_total")
async def history_deals_total(date_from: datetime, date_to: datetime):
    total = mt5.history_deals_total(date_from, date_to)
    return {"total": total}


@app.get("/history_deals_get")
async def history_deals_get(date_from: datetime, date_to: datetime, group: str = None):
    if group:
        deals = mt5.history_deals_get(date_from, date_to, group=group)
    else:
        deals = mt5.history_deals_get(date_from, date_to)
    if deals is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "deals": [d._asdict() for d in deals]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
