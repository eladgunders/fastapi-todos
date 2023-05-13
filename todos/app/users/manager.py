import uuid
from typing import Optional
import logging
from urllib.request import Request

from pydantic import SecretStr
from fastapi_users import BaseUserManager, UUIDIDMixin

from app.core.config import get_config
from app.models.tables import User
from app.utils import send_reset_password_email, send_account_verification_email


config = get_config()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        logger.info('sent reset password email to %s', user.email)

    async def on_after_request_verify(
            self,
            user: User,
            token: str,
            request: Optional[Request] = None
    ) -> None:
        send_account_verification_email(email_to=user.email, token=token)
        logger.info('sent account verification email to %s', user.email)
