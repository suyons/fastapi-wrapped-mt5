from fastapi import APIRouter
import MetaTrader5 as mt5

router = APIRouter(tags=["positions"])


@router.get(
    "/positions_total",
    summary="Get the number of open positions",
    description="Get the number of open positions",
)
async def positions_total():
    return {"total": mt5.positions_total()}


@router.get(
    "/positions_get",
    summary="Get open positions",
    description="Get open positions with the ability to filter by symbol or ticket",
)
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
