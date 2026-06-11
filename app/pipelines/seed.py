"""
Seed pipeline — populates the database with realistic dummy data.
Run with: uv run python -m app.pipelines.seed
"""

import asyncio
from datetime import date, datetime, timedelta
import random

from rich.console import Console
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import (
    Asset, AssetStatus, AssetType,
    Assignment,
    Department,
    Employee,
    MaintenanceLog, MaintenanceType,
)

console = Console()

DEPARTMENTS = [
    {"name": "IT",              "location": "Floor 1"},
    {"name": "HR",              "location": "Floor 2"},
    {"name": "Finance",         "location": "Floor 3"},
    {"name": "Engineering",     "location": "Floor 4"},
    {"name": "Operations",      "location": "Floor 5"},
]

EMPLOYEES = [
    {"first_name": "Alice",   "last_name": "Santos",   "email": "alice.santos@company.com",   "dept": "IT"},
    {"first_name": "Bob",     "last_name": "Reyes",    "email": "bob.reyes@company.com",      "dept": "Engineering"},
    {"first_name": "Carol",   "last_name": "Lim",      "email": "carol.lim@company.com",      "dept": "HR"},
    {"first_name": "David",   "last_name": "Cruz",     "email": "david.cruz@company.com",     "dept": "Finance"},
    {"first_name": "Eva",     "last_name": "Torres",   "email": "eva.torres@company.com",     "dept": "Operations"},
    {"first_name": "Frank",   "last_name": "Garcia",   "email": "frank.garcia@company.com",   "dept": "Engineering"},
    {"first_name": "Grace",   "last_name": "Mendoza",  "email": "grace.mendoza@company.com",  "dept": "IT"},
    {"first_name": "Henry",   "last_name": "Villanueva","email": "henry.villanueva@company.com","dept": "Finance"},
]

ASSETS = [
    {"name": "Dell XPS 15",         "asset_type": AssetType.laptop,  "brand": "Dell",    "model": "XPS 15 9530",   "serial_number": "SN-001", "cost": 1800.00},
    {"name": "MacBook Pro 14",       "asset_type": AssetType.laptop,  "brand": "Apple",   "model": "MBP M3 Pro",    "serial_number": "SN-002", "cost": 2400.00},
    {"name": "ThinkPad X1 Carbon",   "asset_type": AssetType.laptop,  "brand": "Lenovo",  "model": "X1 Carbon G11", "serial_number": "SN-003", "cost": 1600.00},
    {"name": "HP EliteDesk 800",     "asset_type": AssetType.desktop, "brand": "HP",      "model": "EliteDesk 800", "serial_number": "SN-004", "cost": 900.00},
    {"name": "Dell UltraSharp 27",   "asset_type": AssetType.monitor, "brand": "Dell",    "model": "U2723D",        "serial_number": "SN-005", "cost": 600.00},
    {"name": "LG 4K Monitor",        "asset_type": AssetType.monitor, "brand": "LG",      "model": "27UK850-W",     "serial_number": "SN-006", "cost": 450.00},
    {"name": "iPhone 15 Pro",        "asset_type": AssetType.phone,   "brand": "Apple",   "model": "iPhone 15 Pro", "serial_number": "SN-007", "cost": 1100.00},
    {"name": "Samsung Galaxy S24",   "asset_type": AssetType.phone,   "brand": "Samsung", "model": "Galaxy S24",    "serial_number": "SN-008", "cost": 900.00},
    {"name": "iPad Pro 12.9",        "asset_type": AssetType.tablet,  "brand": "Apple",   "model": "iPad Pro M2",   "serial_number": "SN-009", "cost": 1300.00},
    {"name": "Cisco Switch 24-port", "asset_type": AssetType.network, "brand": "Cisco",   "model": "CBS350-24T",    "serial_number": "SN-010", "cost": 700.00},
]


async def seed():
    async with AsyncSessionLocal() as session:

        # Check if already seeded
        result = await session.execute(select(Department))
        if result.scalars().first():
            console.print("[yellow]Database already seeded, skipping.[/yellow]")
            return

        console.print("[bold]Seeding database...[/bold]")

        # 1. Departments
        dept_map = {}
        for d in DEPARTMENTS:
            dept = Department(**d)
            session.add(dept)
            await session.flush()
            dept_map[d["name"]] = dept
        console.print(f"[green]✓[/green] Created {len(DEPARTMENTS)} departments")

        # 2. Employees
        emp_list = []
        for e in EMPLOYEES:
            emp = Employee(
                first_name=e["first_name"],
                last_name=e["last_name"],
                email=e["email"],
                department_id=dept_map[e["dept"]].id,
            )
            session.add(emp)
            await session.flush()
            emp_list.append(emp)
        console.print(f"[green]✓[/green] Created {len(EMPLOYEES)} employees")

        # 3. Assets
        asset_list = []
        for a in ASSETS:
            asset = Asset(
                **a,
                status=AssetStatus.available,
                purchase_date=date.today() - timedelta(days=random.randint(30, 730)),
            )
            session.add(asset)
            await session.flush()
            asset_list.append(asset)
        console.print(f"[green]✓[/green] Created {len(ASSETS)} assets")

        # 4. Assignments — assign first 6 assets to employees
        for i in range(6):
            asset = asset_list[i]
            emp = emp_list[i]
            assignment = Assignment(
                asset_id=asset.id,
                employee_id=emp.id,
                assigned_date=date.today() - timedelta(days=random.randint(1, 180)),
            )
            asset.status = AssetStatus.assigned
            session.add(assignment)
        console.print("[green]✓[/green] Created 6 assignments")

        # 5. Maintenance logs — add 3 maintenance records
        for i in range(3):
            asset = asset_list[i + 6]
            log = MaintenanceLog(
                asset_id=asset.id,
                maintenance_type=random.choice(list(MaintenanceType)),
                description="Routine maintenance check",
                cost=round(random.uniform(50, 300), 2),
                performed_at=datetime.utcnow() - timedelta(days=random.randint(1, 90)),
            )
            asset.status = AssetStatus.maintenance
            session.add(log)
        console.print("[green]✓[/green] Created 3 maintenance logs")

        await session.commit()
        console.print("\n[bold green]✓ Database seeded successfully![/bold green]")


if __name__ == "__main__":
    asyncio.run(seed())