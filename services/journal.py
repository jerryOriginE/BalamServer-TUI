# services/journal.py
import asyncio

async def get_logs(unit: str, lines: int = 200) -> str:
    process = await asyncio.create_subprocess_exec(
        "journalctl",
        "-u", unit,
        "-n", str(lines),
        "--no-pager",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, _ = await process.communicate()
    return stdout.decode(errors="ignore")

async def follow_logs(unit: str):
    procss = await asyncio.create_subprocess_exec(
        "journalctl",
        "-u", unit,
        "-f",
        "--no-pager",
        stdout=asyncio.subprocess.PIPE,
    )

    while True:
        line = await process.stdout.readLine()
        if not line:
            break
        yield line.decode(errors="ignore")