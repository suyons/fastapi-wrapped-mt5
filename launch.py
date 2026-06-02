import os
import subprocess
import sys

from src.config import ACCOUNTS


def main():
    processes = []
    for account in ACCOUNTS:
        env = {**os.environ, "MT5_TERMINAL_PATH": account["path"]}
        p = subprocess.Popen(
            [
                "uv", "run", "uvicorn", "src.main:app",
                "--host", "0.0.0.0",
                "--port", str(account["port"]),
            ],
            env=env,
        )
        print(f"[port {account['port']}] {account['path']}")
        processes.append(p)

    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("\nShutting down all instances...")
        for p in processes:
            p.terminate()


if __name__ == "__main__":
    main()
