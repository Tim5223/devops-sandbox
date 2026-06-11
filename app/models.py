from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Integer, Float, Date, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class AssetStatus(str, enum.Enum):
    available   = "available"
    assigned    = "assigned"
    maintenance = "maintenance"
    retired     = "retired"


class AssetType(str, enum.Enum):
    laptop    = "laptop"
    desktop   = "desktop"
    monitor   = "monitor"
    phone     = "phone"
    tablet    = "tablet"
    server    = "server"
    network   = "network"
    other     = "other"


class MaintenanceType(str, enum.Enum):
    repair    = "repair"
    upgrade   = "upgrade"
    inspection = "inspection"
    replacement = "replacement"


# ── Department ────────────────────────────────────────────────
class Department(Base):
    __tablename__ = "departments"

    id:       Mapped[int]  = mapped_column(Integer, primary_key=True)
    name:     Mapped[str]  = mapped_column(String(100), nullable=False, unique=True)
    location: Mapped[Optional[str]] = mapped_column(String(100))

    employees: Mapped[list["Employee"]] = relationship(back_populates="department")


# ── Employee ──────────────────────────────────────────────────
class Employee(Base):
    __tablename__ = "employees"

    id:            Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name:    Mapped[str] = mapped_column(String(100), nullable=False)
    last_name:     Mapped[str] = mapped_column(String(100), nullable=False)
    email:         Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"))

    department:  Mapped[Optional["Department"]] = relationship(back_populates="employees")
    assignments: Mapped[list["Assignment"]]     = relationship(back_populates="employee")


# ── Asset ─────────────────────────────────────────────────────
class Asset(Base):
    __tablename__ = "assets"

    id:            Mapped[int]   = mapped_column(Integer, primary_key=True)
    name:          Mapped[str]   = mapped_column(String(150), nullable=False)
    asset_type:    Mapped[str]   = mapped_column(Enum(AssetType), nullable=False)
    brand:         Mapped[Optional[str]] = mapped_column(String(100))
    model:         Mapped[Optional[str]] = mapped_column(String(100))
    serial_number: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    status:        Mapped[str]   = mapped_column(Enum(AssetStatus), default=AssetStatus.available)
    purchase_date: Mapped[Optional[date]] = mapped_column(Date)
    cost:          Mapped[Optional[float]] = mapped_column(Float)

    assignments:      Mapped[list["Assignment"]]     = relationship(back_populates="asset")
    maintenance_logs: Mapped[list["MaintenanceLog"]] = relationship(back_populates="asset")


# ── Assignment ────────────────────────────────────────────────
class Assignment(Base):
    __tablename__ = "assignments"

    id:            Mapped[int]  = mapped_column(Integer, primary_key=True)
    asset_id:      Mapped[int]  = mapped_column(ForeignKey("assets.id"), nullable=False)
    employee_id:   Mapped[int]  = mapped_column(ForeignKey("employees.id"), nullable=False)
    assigned_date: Mapped[date] = mapped_column(Date, default=date.today)
    returned_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    notes:         Mapped[Optional[str]]  = mapped_column(Text)

    asset:    Mapped["Asset"]    = relationship(back_populates="assignments")
    employee: Mapped["Employee"] = relationship(back_populates="assignments")


# ── Maintenance Log ───────────────────────────────────────────
class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id:               Mapped[int]      = mapped_column(Integer, primary_key=True)
    asset_id:         Mapped[int]      = mapped_column(ForeignKey("assets.id"), nullable=False)
    maintenance_type: Mapped[str]      = mapped_column(Enum(MaintenanceType), nullable=False)
    description:      Mapped[Optional[str]] = mapped_column(Text)
    cost:             Mapped[Optional[float]] = mapped_column(Float)
    performed_at:     Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    asset: Mapped["Asset"] = relationship(back_populates="maintenance_logs")