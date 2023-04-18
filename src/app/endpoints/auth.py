from fastapi import APIRouter

from db.user import auth_backend, fastapi_users
from db.user_schemas import UserRead, UserCreate, UserUpdate

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(fastapi_users.get_verify_router(UserRead))
router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))
