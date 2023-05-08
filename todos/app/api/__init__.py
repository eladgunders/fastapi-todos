from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.v1 import router as v1_router
from app.core.config import get_config


config = get_config()

router = APIRouter()
router.include_router(v1_router)
router.include_router(health_router)
