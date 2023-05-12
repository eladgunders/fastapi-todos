import uuid
from typing import Optional
from urllib.request import Request

from pydantic import SecretStr
from fastapi_users import BaseUserManager, UUIDIDMixin

from app.core.config import get_config
from app.models.tables import User
from app.utils.emails import send_reset_password_email, send_user_verification_email


config = get_config()


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret: SecretStr = config.JWT_SECRET_KEY
    verification_token_secret: SecretStr = config.JWT_SECRET_KEY

    async def on_after_forgot_password(
            self,
            user: User,
            token: str,
            request: Optional[Request] = None
    ) -> None:
        send_reset_password_email(email_to=user.email, token=token)

    async def on_after_request_verify(
            self,
            user: User,
            token: str,
            request: Optional[Request] = None
    ) -> None:
        send_user_verification_email(email_to=user.email, token=token)
