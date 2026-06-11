from fastapi import APIRouter
from app.api.routers.assets import router as assets_router
from app.api.routers.employees import router as employees_router
from app.api.routers.other import departments_router, assignments_router, maintenance_router

router = APIRouter()

router.include_router(assets_router)
router.include_router(employees_router)
router.include_router(departments_router)
router.include_router(assignments_router)
router.include_router(maintenance_router)
