from fastapi import APIRouter

from app.users.users import fast_api_users
from app.schemas import UserRead, UserUpdate

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

router.include_router(fast_api_users.get_users_router(UserRead, UserUpdate))
