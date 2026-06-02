import os

ACCOUNTS: list[dict] = [
    {
        "path": r"C:\Program Files\MetaTrader 5\terminal64.exe",
        "port": 8001,
    },
    {
        "path": r"C:\Program Files\MetaTrader 5-2\terminal64.exe",
        "port": 8002,
    },
]

MT5_TERMINAL_PATH: str = os.environ.get("MT5_TERMINAL_PATH", "")
