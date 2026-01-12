# widget/postgres_info.py
from textual.widgets import Static
import asyncio
import subprocess

class PostgresInfo(Static):
    BORDER_TITLE = "PostgreSQL"

    def __init__(self):
        super().__init__()
        self.visible = True

    async def show(self):
        self.visible = True
        info = await asyncio.to_thread(self._fetch_info)
        self.update(info)

    async def on_mount(self) -> None:
        await self.show()

    def _fetch_info(self) -> str:
        try:
            def run(sql):
                return subprocess.check_output(
                    ["psql", "-t", "-c", sql],
                    stderr=subprocess.DEVNULL,
                    text=True,
                ).strip()

            version = run("SHOW server_version;")
            conns = run("SELECT count(*) FROM pg_stat_activity;")
            max_conns = run("SHOW max_connections;")
            dbs = run("SELECT count(*) FROM pg_database WHERE datistemplate = false;")
            cache = run("""
                SELECT round(
                    sum(blks_hit) * 100.0 /
                    nullif(sum(blks_hit + blks_read), 0), 1
                )
                FROM pg_stat_database;
            """)

            return (
                f"Version:      {version}\n"
                f"Connections:  {conns} / {max_conns}\n"
                f"Databases:    {dbs}\n"
                f"Cache hit:    {cache or 'N/A'} %"
            )

        except Exception:
            return "Unable to query PostgreSQL"