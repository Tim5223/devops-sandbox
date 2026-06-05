"""
Example pipeline — fetches JSON data from a public API and loads it into PostgreSQL.
Run with: uv run python -m app.pipelines.example_pipeline
"""

import asyncio
import httpx
import pandas as pd
from sqlalchemy import text

from app.database import AsyncSessionLocal
from rich.console import Console

console = Console()


async def extract(url: str) -> list[dict]:
    """Fetch data from an external source."""
    async with httpx.AsyncClient() as client:
        response = client.get(url, timeout=10)
        response.raise_for_status()
        return response.json()


def transform(raw: list[dict]) -> pd.DataFrame:
    """Clean and shape the data."""
    df = pd.DataFrame(raw)
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    return df


async def load(df: pd.DataFrame, table: str) -> None:
    """Write DataFrame rows into PostgreSQL."""
    async with AsyncSessionLocal() as session:
        for _, row in df.iterrows():
            cols = ", ".join(row.index)
            vals = ", ".join([f":{k}" for k in row.index])
            stmt = text(f"INSERT INTO {table} ({cols}) VALUES ({vals}) ON CONFLICT DO NOTHING")
            await session.execute(stmt, row.to_dict())
        await session.commit()
    console.print(f"[green]✓[/green] Loaded {len(df)} rows into [bold]{table}[/bold]")


async def run() -> None:
    console.print("[bold]Starting example pipeline...[/bold]")
    raw = await extract("https://jsonplaceholder.typicode.com/todos")
    df = transform(raw)
    console.print(df.head())
    # await load(df, "todos")   # Uncomment once todos table exists


if __name__ == "__main__":
    asyncio.run(run())
