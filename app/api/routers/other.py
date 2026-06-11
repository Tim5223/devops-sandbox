from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import Department, Assignment, MaintenanceLog, Asset, AssetStatus
from app.schemas import (
    DepartmentCreate, DepartmentRead,
    AssignmentCreate, AssignmentRead,
    MaintenanceLogCreate, MaintenanceLogRead,
)
from sqlalchemy.orm import selectinload

# ── Departments ───────────────────────────────────────────────
departments_router = APIRouter(prefix="/departments", tags=["Departments"])

@departments_router.get("/", response_model=list[DepartmentRead])
async def list_departments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department))
    return result.scalars().all()

@departments_router.post("/", response_model=DepartmentRead, status_code=201)
async def create_department(payload: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    dept = Department(**payload.model_dump())
    db.add(dept)
    await db.commit()
    await db.refresh(dept)
    return dept

@departments_router.delete("/{dept_id}", status_code=204)
async def delete_department(dept_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department).where(Department.id == dept_id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    await db.delete(dept)
    await db.commit()


# ── Assignments ───────────────────────────────────────────────
assignments_router = APIRouter(prefix="/assignments", tags=["Assignments"])

@assignments_router.get("/", response_model=list[AssignmentRead])
async def list_assignments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Assignment).options(
            selectinload(Assignment.asset),
            selectinload(Assignment.employee)
        )
    )
    return result.scalars().all()

@assignments_router.post("/", response_model=AssignmentRead, status_code=201)
async def create_assignment(payload: AssignmentCreate, db: AsyncSession = Depends(get_db)):
    assignment = Assignment(**payload.model_dump())
    # Mark asset as assigned
    asset_result = await db.execute(select(Asset).where(Asset.id == payload.asset_id))
    asset = asset_result.scalar_one_or_none()
    if asset:
        asset.status = AssetStatus.assigned
    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)
    return assignment

@assignments_router.put("/{assignment_id}/return", response_model=AssignmentRead)
async def return_asset(assignment_id: int, db: AsyncSession = Depends(get_db)):
    from datetime import date
    result = await db.execute(
        select(Assignment)
        .where(Assignment.id == assignment_id)
        .options(selectinload(Assignment.asset), selectinload(Assignment.employee))
    )
    assignment = result.scalar_one_or_none()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    assignment.returned_date = date.today()
    assignment.asset.status = AssetStatus.available
    await db.commit()
    await db.refresh(assignment)
    return assignment


# ── Maintenance Logs ──────────────────────────────────────────
maintenance_router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

@maintenance_router.get("/", response_model=list[MaintenanceLogRead])
async def list_maintenance(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MaintenanceLog).options(selectinload(MaintenanceLog.asset))
    )
    return result.scalars().all()

@maintenance_router.post("/", response_model=MaintenanceLogRead, status_code=201)
async def create_maintenance_log(payload: MaintenanceLogCreate, db: AsyncSession = Depends(get_db)):
    log = MaintenanceLog(**payload.model_dump())
    # Mark asset as in maintenance
    asset_result = await db.execute(select(Asset).where(Asset.id == payload.asset_id))
    asset = asset_result.scalar_one_or_none()
    if asset:
        asset.status = AssetStatus.maintenance
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log
