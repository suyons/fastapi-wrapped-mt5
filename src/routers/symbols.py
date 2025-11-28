from fastapi import APIRouter
import MetaTrader5 as mt5

router = APIRouter(tags=["symbols"])


@router.get(
    "/symbols_total",
    summary="Get total number of symbols",
    description="Get the number of all financial instruments in the MetaTrader 5 terminal",
)
async def symbols_total():
    return {"total": mt5.symbols_total()}


@router.get(
    "/symbols_get",
    summary="Get all financial instruments",
    description="Get all financial instruments from the MetaTrader 5 terminal e.g. `*BTC*` to get all symbols containing **BTC**",
)
async def symbols_get(group: str = None):
    if group:
        symbols = mt5.symbols_get(group)
    else:
        symbols = mt5.symbols_get()
    if symbols is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"symbols": [s._asdict() for s in symbols]}


@router.get(
    "/symbol_info/{symbol}",
    summary="Get data on a specified financial instrument",
    description="Get data on the specified financial instrument",
)
async def symbol_info(symbol: str):
    info = mt5.symbol_info(symbol)
    if info is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "info": info._asdict()}


@router.get(
    "/symbol_info_tick/{symbol}",
    summary="Get the last tick for a financial instrument",
    description="Get the last tick for the specified financial instrument",
)
async def symbol_info_tick(symbol: str):
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "tick": tick._asdict()}


@router.post(
    "/symbol_select/{symbol}",
    summary="Select or remove a symbol in MarketWatch",
    description="Select a symbol in the MarketWatch window or remove a symbol from the window",
)
async def symbol_select(symbol: str, enable: bool):
    if not mt5.symbol_select(symbol, enable):
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success"}
