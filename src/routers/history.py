from datetime import datetime
from typing import Optional
from fastapi import APIRouter
import MetaTrader5 as mt5

router = APIRouter(tags=["history"])


@router.get(
    "/history_orders_total",
    summary="Get the number of orders in trading history",
    description="Get the number of orders in trading history within the specified interval",
)
async def history_orders_total(date_from: datetime, date_to: datetime):
    total = mt5.history_orders_total(date_from, date_to)
    return {"total": total}


@router.get(
    "/history_orders_get",
    summary="Get orders from trading history",
    description="Get orders from trading history. Filter by `group` (e.g. `*USD*`), `ticket` (order ticket), or `position` (position ID).",
)
async def history_orders_get(
    date_from: datetime,
    date_to: datetime,
    group: str = None,
    ticket: int = None,
    position: int = None,
):
    if ticket is not None:
        orders = mt5.history_orders_get(ticket=ticket)
    elif position is not None:
        orders = mt5.history_orders_get(position=position)
    elif group:
        orders = mt5.history_orders_get(date_from, date_to, group=group)
    else:
        orders = mt5.history_orders_get(date_from, date_to)
    if orders is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "orders": [o._asdict() for o in orders]}


@router.get(
    "/history_deals_total",
    summary="Get the number of deals in trading history",
    description="Get the number of deals in trading history within the specified interval",
)
async def history_deals_total(date_from: datetime, date_to: datetime):
    total = mt5.history_deals_total(date_from, date_to)
    return {"total": total}


@router.get(
    "/history_deals_get",
    summary="Get deals from trading history",
    description="Get deals from trading history. Filter by `group` (e.g. `*USD*`), `ticket` (deal ticket), or `position` (position ID).",
)
async def history_deals_get(
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    group: str = None,
    ticket: int = None,
    position: int = None,
):
    if ticket is not None:
        deals = mt5.history_deals_get(ticket=ticket)
    elif position is not None:
        deals = mt5.history_deals_get(position=position)
    elif group and date_from and date_to:
        deals = mt5.history_deals_get(date_from, date_to, group=group)
    elif date_from and date_to:
        deals = mt5.history_deals_get(date_from, date_to)
    else:
        return {"status": "failed", "error": "date_from and date_to required when not filtering by ticket or position"}
    if deals is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "deals": [d._asdict() for d in deals]}
