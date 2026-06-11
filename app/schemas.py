from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models import AssetStatus, AssetType, MaintenanceType


# ── Department ────────────────────────────────────────────────
class DepartmentBase(BaseModel):
    name: str
    location: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentRead(DepartmentBase):
    id: int
    model_config = {"from_attributes": True}


# ── Employee ──────────────────────────────────────────────────
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department_id: Optional[int] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeRead(EmployeeBase):
    id: int
    department: Optional[DepartmentRead] = None
    model_config = {"from_attributes": True}


# ── Asset ─────────────────────────────────────────────────────
class AssetBase(BaseModel):
    name: str
    asset_type: AssetType
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    status: AssetStatus = AssetStatus.available
    purchase_date: Optional[date] = None
    cost: Optional[float] = None

class AssetCreate(AssetBase):
    pass

class AssetRead(AssetBase):
    id: int
    model_config = {"from_attributes": True}


# ── Assignment ────────────────────────────────────────────────
class AssignmentBase(BaseModel):
    asset_id: int
    employee_id: int
    assigned_date: date = date.today()
    returned_date: Optional[date] = None
    notes: Optional[str] = None

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentRead(AssignmentBase):
    id: int
    asset: AssetRead
    employee: EmployeeRead
    model_config = {"from_attributes": True}


# ── Maintenance Log ───────────────────────────────────────────
class MaintenanceLogBase(BaseModel):
    asset_id: int
    maintenance_type: MaintenanceType
    description: Optional[str] = None
    cost: Optional[float] = None
    performed_at: datetime = datetime.utcnow()

class MaintenanceLogCreate(MaintenanceLogBase):
    pass

class MaintenanceLogRead(MaintenanceLogBase):
    id: int
    asset: AssetRead
    model_config = {"from_attributes": True}