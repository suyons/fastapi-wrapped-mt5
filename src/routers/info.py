from fastapi import APIRouter
import MetaTrader5 as mt5

router = APIRouter(tags=["info"])


@router.get(
    "/version",
    summary="Get MetaTrader 5 terminal version",
    description="Return the MetaTrader 5 terminal version",
)
async def version():
    return {"version": mt5.version()}


@router.get(
    "/last_error",
    summary="Get the last error",
    description="Return data on the last error",
)
async def last_error():
    return {"last_error": mt5.last_error()}


@router.get(
    "/account_info",
    summary="Get account information",
    description="Get info on the current trading account",
)
async def account_info():
    info = mt5.account_info()
    if info is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "info": info._asdict()}


@router.get(
    "/terminal_info",
    summary="Get terminal information",
    description="Get status and parameters of the connected MetaTrader 5 terminal",
)
async def terminal_info():
    info = mt5.terminal_info()
    if info is None:
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success", "info": info._asdict()}
