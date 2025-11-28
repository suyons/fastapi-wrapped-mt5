from datetime import datetime
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
    description="Get orders from trading history with the ability to filter by ticket or position",
)
async def history_orders_get(date_from: datetime, date_to: datetime, group: str = None):
    if group:
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
    description="Get deals from trading history with the ability to filter by ticket or position",
)
async def history_deals_get(date_from: datetime, date_to: datetime, group: str = None):
    if group:
        deals = mt5.history_deals_get(date_from, date_to, group=group)
    else:
        deals = mt5.history_deals_get(date_from, date_to)
    if deals is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "deals": [d._asdict() for d in deals]}
