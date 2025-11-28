from datetime import datetime
from fastapi import APIRouter
import MetaTrader5 as mt5

from src.models import TimeFrame
from src.utils import structured_array_to_list

router = APIRouter(tags=["market_data"])


@router.post(
    "/market_book_add/{symbol}",
    summary="Subscribe to Market Depth change events",
    description="Subscribes the MetaTrader 5 terminal to the Market Depth change events for a specified symbol",
)
async def market_book_add(symbol: str):
    if not mt5.market_book_add(symbol):
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success"}


@router.get(
    "/market_book_get/{symbol}",
    summary="Get Market Depth entries for a symbol",
    description="Returns a tuple from BookInfo featuring Market Depth entries for the specified symbol",
)
async def market_book_get(symbol: str):
    book = mt5.market_book_get(symbol)
    if book is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "book": book}


@router.post(
    "/market_book_release/{symbol}",
    summary="Cancel Market Depth subscription",
    description="Cancels subscription of the MetaTrader 5 terminal to the Market Depth change events for a specified symbol",
)
async def market_book_release(symbol: str):
    if not mt5.market_book_release(symbol):
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success"}


@router.get(
    "/copy_rates_from/{symbol}",
    summary="Get bars from a specified date",
    description="Get bars from the MetaTrader 5 terminal starting from the specified date (in ISO 8601 format) e.g. `date_from=2025-11-11T00:00:00`",
)
async def copy_rates_from(
    symbol: str, timeframe: TimeFrame, date_from: datetime, count: int
):
    rates = mt5.copy_rates_from(symbol, timeframe.value, date_from, count)
    if rates is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "rates": structured_array_to_list(rates)}


@router.get(
    "/copy_rates_from_pos/{symbol}",
    summary="Get bars from a specified index",
    description="Get bars from the MetaTrader 5 terminal starting from the specified index (0 = the latest bar)",
)
async def copy_rates_from_pos(
    symbol: str, timeframe: TimeFrame, start_pos: int, count: int
):
    rates = mt5.copy_rates_from_pos(symbol, timeframe.value, start_pos, count)
    if rates is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "rates": structured_array_to_list(rates)}


@router.get(
    "/copy_rates_range/{symbol}",
    summary="Get bars in a specified date range",
    description="Get bars in the specified date range from the MetaTrader 5 terminal",
)
async def copy_rates_range(
    symbol: str, timeframe: TimeFrame, date_from: datetime, date_to: datetime
):
    rates = mt5.copy_rates_range(symbol, timeframe.value, date_from, date_to)
    if rates is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "rates": structured_array_to_list(rates)}


@router.get(
    "/copy_ticks_from/{symbol}",
    summary="Get ticks from a specified date",
    description="Get ticks from the MetaTrader 5 terminal starting from the specified date",
)
async def copy_ticks_from(symbol: str, date_from: datetime, count: int, flags: int):
    ticks = mt5.copy_ticks_from(symbol, date_from, count, flags)
    if ticks is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "ticks": structured_array_to_list(ticks)}


@router.get(
    "/copy_ticks_range/{symbol}",
    summary="Get ticks for a specified date range",
    description="Get ticks for the specified date range from the MetaTrader 5 terminal",
)
async def copy_ticks_range(
    symbol: str, date_from: datetime, date_to: datetime, flags: int
):
    ticks = mt5.copy_ticks_range(symbol, date_from, date_to, flags)
    if ticks is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "ticks": structured_array_to_list(ticks)}
