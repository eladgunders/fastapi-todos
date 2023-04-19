from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.priorities import router as priorities_router
from app.api.categories import router as categories_router

router = APIRouter()

router.include_router(health_router)
router.include_router(auth_router)
router.include_router(priorities_router)
router.include_router(categories_router)
