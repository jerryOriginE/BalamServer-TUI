# services/journal.py
import asyncio
import contextlib
from typing import AsyncIterator

JOURNAL_FORMAT = ["-o", "short-iso", "--no-pager"]

async def get_recent_logs(unit: str, lines: int = 50) -> list[str]:
    try:
        process = await asyncio.create_subprocess_exec(
            "journalctl",
            "-u", unit,
            "-n", str(lines),
            *JOURNAL_FORMAT,
            stdout=asyncio.subprocess.PIPE,
        )

        stdout, _ = await process.communicate()
        log_lines = stdout.decode(errors="ignore").splitlines() 
        return log_lines if log_lines else ["No logs available"]
    except FileNotFoundError:
        return ["journalctl not found"]
    except Exception as e:
        return [f"Failed to get logs: {e}"] 
