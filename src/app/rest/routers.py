from fastapi import APIRouter, status

from app.rest import auth

router = APIRouter()

router.include_router(auth.router)


@router.get('/healthcheck', status_code=status.HTTP_200_OK)
async def healthcheck():
    return
