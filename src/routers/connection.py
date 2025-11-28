from fastapi import APIRouter
import MetaTrader5 as mt5

from src.models import LoginRequest

router = APIRouter(tags=["connection"])


@router.post(
    "/initialize",
    summary="Initialize MetaTrader 5 connection",
    description="Establish a connection with the MetaTrader 5 terminal",
)
async def initialize():
    if not mt5.initialize():
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success"}


@router.post(
    "/login",
    summary="Login to a trading account",
    description="Connect to a trading account using specified parameters",
)
async def login(login_request: LoginRequest):
    if not mt5.login(
        login_request.account,
        password=login_request.password,
        server=login_request.server,
    ):
        return {"status": "failed", "error": mt5.last_error()}
    return {"status": "success"}


@router.post(
    "/shutdown",
    summary="Shutdown MetaTrader 5 connection",
    description="Close the previously established connection to the MetaTrader 5 terminal",
)
async def shutdown():
    mt5.shutdown()
    return {"status": "success"}
