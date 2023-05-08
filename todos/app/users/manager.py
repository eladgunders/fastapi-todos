import uuid

from pydantic import SecretStr
from fastapi_users import BaseUserManager, UUIDIDMixin

from app.core.config import get_config
from app.models.tables import User


config = get_config()


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret: SecretStr = config.JWT_SECRET_KEY
    verification_token_secret: SecretStr = config.JWT_SECRET_KEY
