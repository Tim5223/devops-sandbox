"""
Sandbox CLI — run with: uv run sandbox <command>
"""

import asyncio
import typer
from rich.console import Console
from rich import print as rprint
from sqlalchemy import text

from app.database import AsyncSessionLocal

app = typer.Typer(help="DevOps sandbox CLI")
console = Console()


@app.command()
def ping():
    """Check PostgreSQL connectivity."""
    async def _ping():
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT version()"))
            version = result.scalar()
            rprint(f"[green]✓ Connected![/green] {version}")

    asyncio.run(_ping())


@app.command()
def healthcheck():
    """Query the healthcheck table."""
    async def _check():
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT * FROM healthcheck ORDER BY id DESC LIMIT 5"))
            rows = result.fetchall()
            for row in rows:
                console.print(row)

    asyncio.run(_check())


if __name__ == "__main__":
    app()
