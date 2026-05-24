from fastapi import APIRouter
import MetaTrader5 as mt5

from src.models import OrderRequest, OrderType, TradeRequestActions
from src.utils import resolve_filling

router = APIRouter(tags=["orders"])


@router.get(
    "/orders_total",
    summary="Get the number of active orders",
    description="Get the number of active orders",
)
async def orders_total():
    return {"total": mt5.orders_total()}


@router.get(
    "/orders_get",
    summary="Get active orders",
    description="Get active orders with the ability to filter by symbol or ticket",
)
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


@router.post(
    "/order_calc_margin",
    summary="Calculate margin for a trading operation",
    description="Return margin in the account currency to perform a specified trading operation. Provide `type` (0=BUY, 1=SELL), `symbol`, `volume`, and `price`.",
)
async def order_calc_margin(order_request: OrderRequest):
    margin = mt5.order_calc_margin(
        order_request.type,
        order_request.symbol,
        order_request.volume,
        order_request.price,
    )
    if margin is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "margin": margin}


@router.post(
    "/order_calc_profit",
    summary="Calculate profit for a trading operation",
    description="Return profit in the account currency. Provide `type` (0=BUY, 1=SELL), `symbol`, `volume`, `price` (open price), and `tp` (close/target price).",
)
async def order_calc_profit(order_request: OrderRequest):
    profit = mt5.order_calc_profit(
        order_request.type,
        order_request.symbol,
        order_request.volume,
        order_request.price,
        order_request.tp,
    )
    if profit is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "profit": profit}


@router.post(
    "/order_check",
    summary="Check funds sufficiency for a trading operation",
    description="Check funds sufficiency for performing a required trading operation",
)
async def order_check(order_request: OrderRequest):
    info = mt5.symbol_info(order_request.symbol)
    if info is None:
        return {"status": "failed", "error": f"Symbol {order_request.symbol} not found"}

    request_dict = {k: v for k, v in order_request.model_dump().items() if v is not None}
    request_dict["type_filling"] = resolve_filling(info, order_request.type_filling)

    if order_request.type in (mt5.ORDER_TYPE_BUY, mt5.ORDER_TYPE_SELL):
        request_dict["action"] = mt5.TRADE_ACTION_DEAL
    else:
        request_dict["action"] = mt5.TRADE_ACTION_PENDING

    result = mt5.order_check(request_dict)
    if result is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "result": result._asdict()}


@router.post(
    "/order_send",
    summary="Send a request to perform a trading operation",
    description="Send a request to perform a trading operation from open to close and SL/TP modification",
)
async def order_send(order_request: OrderRequest):
    info = mt5.symbol_info(order_request.symbol)
    if info is None:
        return {"status": "failed", "error": f"Symbol {order_request.symbol} not found"}

    tick = mt5.symbol_info_tick(order_request.symbol)
    if tick is None:
        return {"status": "failed", "error": f"Failed to get tick info for {order_request.symbol}"}

    request_dict = {k: v for k, v in order_request.model_dump().items() if v is not None}

    if order_request.position is not None:
        positions = mt5.positions_get(ticket=order_request.position)
        if not positions:
            return {"status": "failed", "error": f"Position {order_request.position} not found"}
        pos = positions[0]

        has_sltp = (order_request.sl and order_request.sl > 0) or (order_request.tp and order_request.tp > 0)
        if has_sltp:
            # SL/TP modification
            request_dict["action"] = mt5.TRADE_ACTION_SLTP
            request_dict["price"] = pos.price_open
            request_dict["volume"] = pos.volume
        else:
            # Close position
            if pos.type == mt5.POSITION_TYPE_BUY:
                request_dict["type"] = mt5.ORDER_TYPE_SELL
                request_dict["price"] = tick.bid
            else:
                request_dict["type"] = mt5.ORDER_TYPE_BUY
                request_dict["price"] = tick.ask
            request_dict["action"] = mt5.TRADE_ACTION_DEAL
            request_dict["symbol"] = pos.symbol
            request_dict["volume"] = order_request.volume if order_request.volume > 0 else pos.volume
            request_dict["type_filling"] = resolve_filling(info, order_request.type_filling)
    elif order_request.type in (mt5.ORDER_TYPE_BUY, mt5.ORDER_TYPE_SELL):
        # Market order
        current_price = tick.ask if order_request.type == mt5.ORDER_TYPE_BUY else tick.bid
        min_dist = info.trade_stops_level * info.point

        if request_dict.get("sl", 0.0) > 0:
            sl = round(request_dict["sl"], info.digits)
            if order_request.type == mt5.ORDER_TYPE_BUY and sl >= current_price:
                return {"status": "failed", "error": "For BUY order, SL must be below current price"}
            if order_request.type == mt5.ORDER_TYPE_SELL and sl <= current_price:
                return {"status": "failed", "error": "For SELL order, SL must be above current price"}
            if min_dist and abs(current_price - sl) < min_dist:
                return {"status": "failed", "error": f"SL too close to current price (min distance: {min_dist})"}
            request_dict["sl"] = sl

        if request_dict.get("tp", 0.0) > 0:
            tp = round(request_dict["tp"], info.digits)
            if order_request.type == mt5.ORDER_TYPE_BUY and tp <= current_price:
                return {"status": "failed", "error": "For BUY order, TP must be above current price"}
            if order_request.type == mt5.ORDER_TYPE_SELL and tp >= current_price:
                return {"status": "failed", "error": "For SELL order, TP must be below current price"}
            if min_dist and abs(current_price - tp) < min_dist:
                return {"status": "failed", "error": f"TP too close to current price (min distance: {min_dist})"}
            request_dict["tp"] = tp

        request_dict["action"] = mt5.TRADE_ACTION_DEAL
        request_dict["type_filling"] = resolve_filling(info, order_request.type_filling)
    else:
        # Pending order
        request_dict["action"] = mt5.TRADE_ACTION_PENDING
        request_dict["type_filling"] = resolve_filling(info, order_request.type_filling)

    result = mt5.order_send(request_dict)
    if result is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "result": result._asdict()}
