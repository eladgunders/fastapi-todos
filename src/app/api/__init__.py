from fastapi import APIRouter

from app.api import health, auth, categories

router = APIRouter()

router.include_router(health.router)
router.include_router(auth.router)
router.include_router(categories.router)
