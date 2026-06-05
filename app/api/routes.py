from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter()


@router.get("/ping-db")
async def ping_db(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Verify the API can reach PostgreSQL."""
    result = await db.execute(text("SELECT NOW()"))
    ts = result.scalar()
    return {"db_time": str(ts)}
