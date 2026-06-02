# CLAUDE.md

## Project overview

FastAPI wrapper around the MetaTrader 5 Python library. Exposes MT5 functionality as a REST API so any OS can interact with a Windows MT5 terminal over HTTP.

The MT5 Python library uses **global state per process** — one process = one terminal connection. Multiple terminals require multiple processes.

## Running the project

```powershell
./start.ps1          # launches all instances defined in src/config.py
```

Internally, `start.ps1` calls `uv run python -m src.launch`. `src/launch.py` reads `ACCOUNTS` from `src/config.py` and spawns one uvicorn subprocess per entry, injecting `MT5_TERMINAL_PATH` as an environment variable.

> Note: must be run as a module (`-m src.launch`) — running `python src/launch.py` directly fails because Python would put `src/` on `sys.path` instead of the project root, breaking `from src.config import ACCOUNTS`.

To run a single instance manually:

```powershell
$env:MT5_TERMINAL_PATH = "C:\Program Files\MetaTrader 5\terminal64.exe"
uv run uvicorn src.main:app --host 0.0.0.0 --port 8001
```

## Key files

| File | Purpose |
|------|---------|
| `src/config.py` | `ACCOUNTS` list — defines terminal path and port per instance |
| `src/launch.py` | Reads `ACCOUNTS`, spawns one uvicorn process per entry |
| `src/main.py` | FastAPI app assembly — mounts all routers |
| `src/models.py` | Pydantic models and MT5 enum wrappers |
| `src/utils.py` | `structured_array_to_list` for numpy results, `resolve_filling` for order fill mode |
| `src/routers/connection.py` | `/initialize`, `/login`, `/shutdown` — always call initialize first |
| `src/routers/orders.py` | Order placement, margin/profit calc, SL/TP modification, position close |

## Adding a new terminal

Edit `src/config.py` and append to `ACCOUNTS`:

```python
ACCOUNTS: list[dict] = [
    {"path": r"C:\Program Files\MetaTrader 5\terminal64.exe",   "port": 8001},
    {"path": r"C:\Program Files\MetaTrader 5-2\terminal64.exe", "port": 8002},
    {"path": r"C:\Program Files\MetaTrader 5-3\terminal64.exe", "port": 8003},  # new
]
```

No other changes needed.

## Adding a new endpoint

1. Add the route function to the appropriate file under `src/routers/`.
2. The router is already mounted in `src/main.py` — no registration needed for existing routers.
3. For a new router file, import and mount it in `src/main.py` following the existing pattern.

## MT5 connection lifecycle

Every instance must follow this sequence before any data endpoints work:

```
POST /initialize   →  connects to the terminal at MT5_TERMINAL_PATH
POST /login        →  authenticates with broker (account, password, server)
... use API ...
POST /shutdown     →  closes connection
```

`mt5.initialize()` accepts an optional `path` argument (set from `MT5_TERMINAL_PATH`). If the env var is empty, MT5 connects to whatever terminal is currently running.

## Dependencies

Managed with `uv`. Add packages via `uv add <package>`. The runtime requires Python ≥ 3.13 and Windows (MT5 Python library is Windows-only).
