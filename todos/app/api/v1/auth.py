from fastapi import APIRouter

from app.users.users import fast_api_users
from app.users.auth import auth_backend
from app.schemas import UserRead, UserCreate

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


router.include_router(fast_api_users.get_register_router(UserRead, UserCreate))
router.include_router(fast_api_users.get_auth_router(auth_backend))
router.include_router(fast_api_users.get_reset_password_router())
router.include_router(fast_api_users.get_verify_router(UserRead))
