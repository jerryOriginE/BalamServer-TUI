# services/journal.py
import asyncio
import contextlib
from typing import AsyncIterator

JOURNAL_FORMAT = ["-o", "short-iso", "--no-pager"]

async def get_recent_logs(unit: str, lines: int = 50) -> list[str]:
    process = await asyncio.create_subprocess_exec(
        "journalctl",
        "-u", unit,
        "-n", str(lines),
        *JOURNAL_FORMAT,
        stdout=asyncio.subprocess.PIPE,
    )

    stdout, _ = await process.communicate()
    return stdout.decode(errors="ignore").splitlines()

async def follow_logs(unit: str) -> AsyncIterator[str]:
    process = await asyncio.create_subprocess_exec(
        "journalctl",
        "-u", unit,
        "-f",
        *JOURNAL_FORMAT,
        stdout=asyncio.subprocess.PIPE,
    )

    try:
        assert process.stdout is not None
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            yield line.decode(errors="ignore").rstrip()
    except asyncio.CancelledError:
        pass
    finally:
        process.terminate()
        with contextlib.suppress(ProcessLookupError):
            await process.wait()


async def get_recent_logs(unit: str, lines: int = 30) -> list[str]:
    process = await asyncio.create_subprocess_exec(
        "journalctl",
        "-u", unit,
        "-n", str(lines),
        "--no-pager",
        stdout=asyncio.subprocess.PIPE,
    )

    stdout, _ = await process.communicate()
    log_lines = stdout.decode(errors="ignore").splitlines()
    return log_lines