import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.api.auth.deps import get_user_manager
from app.models.tables import User
from app.core.security import auth_backend
from app.schemas import UserRead, UserCreate, UserUpdate

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

fast_api_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])


router.include_router(fast_api_users.get_register_router(UserRead, UserCreate))
router.include_router(fast_api_users.get_auth_router(auth_backend))
router.include_router(fast_api_users.get_reset_password_router())
router.include_router(fast_api_users.get_verify_router(UserRead))
router.include_router(fast_api_users.get_users_router(UserRead, UserUpdate))