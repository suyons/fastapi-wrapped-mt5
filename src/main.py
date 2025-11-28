from fastapi import FastAPI

from src.routers import (
    connection,
    history,
    info,
    market_data,
    orders,
    positions,
    symbols,
)

app = FastAPI(
    title="fastapi-wrapped-mt5",
    description="A FastAPI application to interact with MetaTrader 5",
)

app.include_router(connection.router)
app.include_router(history.router)
app.include_router(info.router)
app.include_router(market_data.router)
app.include_router(orders.router)
app.include_router(positions.router)
app.include_router(symbols.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
