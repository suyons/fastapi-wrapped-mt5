from fastapi import APIRouter
import MetaTrader5 as mt5

from src.models import OrderRequest, OrderType

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
    description="Return margin in the account currency to perform a specified trading operation",
)
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


@router.post(
    "/order_calc_profit",
    summary="Calculate profit for a trading operation",
    description="Return profit in the account currency for a specified trading operation",
)
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


@router.post(
    "/order_check",
    summary="Check funds sufficiency for a trading operation",
    description="Check funds sufficiency for performing a required trading operation",
)
async def order_check(order_request: OrderRequest):
    info = mt5.symbol_info(order_request.symbol)
    if info is None:
        return {"status": "failed", "error": f"Symbol {order_request.symbol} not found"}

    request_dict = order_request.model_dump()
    request_dict = {k: v for k, v in request_dict.items() if v is not None}

    filling_mode = info.filling_mode
    req_filling_type = order_request.type_filling

    if req_filling_type == mt5.ORDER_FILLING_FOK and not (
        filling_mode & mt5.ORDER_FILLING_FOK
    ):
        if filling_mode & mt5.ORDER_FILLING_IOC:
            request_dict["type_filling"] = mt5.ORDER_FILLING_IOC
    elif req_filling_type == mt5.ORDER_FILLING_IOC and not (
        filling_mode & mt5.ORDER_FILLING_IOC
    ):
        if filling_mode & mt5.ORDER_FILLING_FOK:
            request_dict["type_filling"] = mt5.ORDER_FILLING_FOK

    if order_request.type in [OrderType.ORDER_TYPE_BUY, OrderType.ORDER_TYPE_SELL]:
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
    description="Send a request to perform a trading operation",
)
async def order_send(order_request: OrderRequest):
    info = mt5.symbol_info(order_request.symbol)
    if info is None:
        return {"status": "failed", "error": f"Symbol {order_request.symbol} not found"}

    tick = mt5.symbol_info_tick(order_request.symbol)
    if tick is None:
        return {"status": "failed", "error": f"Failed to get tick info for {order_request.symbol}"}

    current_price = 0.0
    if order_request.type == OrderType.ORDER_TYPE_BUY:
        current_price = tick.ask
    elif order_request.type == OrderType.ORDER_TYPE_SELL:
        current_price = tick.bid
    # For other order types (e.g., pending orders), current_price might be order_request.price or similar.
    # For simplicity, we'll focus on market orders for now.

    # Minimum distance for SL/TP from current price
    info_dict = info._asdict()
    stops_level = info_dict.get("stops_level")

    min_stop_distance = 0.0 # Default to 0, if stops_level is not available
    if stops_level is not None:
        min_stop_distance = stops_level * info.point
    else:
        print(f"Warning: stops_level information not available for symbol {order_request.symbol}. Proceeding without this specific validation.")

    request_dict = order_request.model_dump()
    request_dict = {k: v for k, v in request_dict.items() if v is not None}

    # Validate and adjust SL/TP if provided
    if request_dict.get("sl", 0) > 0:
        sl = request_dict["sl"]
        # Round SL to symbol's digits
        sl = round(sl, info.digits)

        # Directional check for SL
        if order_request.type == OrderType.ORDER_TYPE_BUY and sl >= current_price:
            return {"status": "failed", "error": "For BUY order, SL must be below current price."}
        elif order_request.type == OrderType.ORDER_TYPE_SELL and sl <= current_price:
            return {"status": "failed", "error": "For SELL order, SL must be above current price."}

        # Check min_stop_distance for SL
        if abs(current_price - sl) < min_stop_distance:
            return {"status": "failed", "error": f"SL is too close to current price. Minimum distance: {min_stop_distance}"}
        
        request_dict["sl"] = sl # Update with rounded value

    if request_dict.get("tp", 0) > 0:
        tp = request_dict["tp"]
        # Round TP to symbol's digits
        tp = round(tp, info.digits)

        # Directional check for TP
        if order_request.type == OrderType.ORDER_TYPE_BUY and tp <= current_price:
            return {"status": "failed", "error": "For BUY order, TP must be above current price."}
        elif order_request.type == OrderType.ORDER_TYPE_SELL and tp >= current_price:
            return {"status": "failed", "error": "For SELL order, TP must be below current price."}

        # Check min_stop_distance for TP
        if abs(current_price - tp) < min_stop_distance:
            return {"status": "failed", "error": f"TP is too close to current price. Minimum distance: {min_stop_distance}"}

        request_dict["tp"] = tp # Update with rounded value

    filling_mode = info.filling_mode
    req_filling_type = order_request.type_filling

    if req_filling_type == mt5.ORDER_FILLING_FOK and not (
        filling_mode & mt5.ORDER_FILLING_FOK
    ):
        if filling_mode & mt5.ORDER_FILLING_IOC:
            request_dict["type_filling"] = mt5.ORDER_FILLING_IOC
    elif req_filling_type == mt5.ORDER_FILLING_IOC and not (
        filling_mode & mt5.ORDER_FILLING_IOC
    ):
        if filling_mode & mt5.ORDER_FILLING_FOK:
            request_dict["type_filling"] = mt5.ORDER_FILLING_FOK

    if order_request.type in [OrderType.ORDER_TYPE_BUY, OrderType.ORDER_TYPE_SELL]:
        request_dict["action"] = mt5.TRADE_ACTION_DEAL
    else:
        request_dict["action"] = mt5.TRADE_ACTION_PENDING

    result = mt5.order_send(request_dict)
    if result is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "result": result._asdict()}
