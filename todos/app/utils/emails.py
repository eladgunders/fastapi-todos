from typing import Any, Optional
import logging

from emails import Message
from emails.template import JinjaTemplate

from app.core.config import get_config


config = get_config()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_email(
    *,
    email_to: str,
    environment: Optional[dict[str, Any]],
    subject_template: str = "",
    html_template: str = "",
) -> None:
    assert config.EMAILS_ENABLED, 'no configuration provided for email variables'
    if not environment:
        environment = {}
    message = Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(config.EMAILS_FROM_NAME, config.EMAILS_FROM_EMAIL),
    )
    smtp_options = {'host': config.SMTP_HOST, 'port': config.SMTP_PORT}
    if config.SMTP_TLS:
        smtp_options['tls'] = True
    if config.SMTP_USER:
        smtp_options['user'] = config.SMTP_USER
    if config.SMTP_PASSWORD:
        smtp_options['password'] = config.SMTP_PASSWORD.get_secret_value()
    res = message.send(to=email_to, render=environment, smtp=smtp_options)
    logger.info('send email result %s', res)


def send_reset_password_email(*, email_to: str, token: str) -> None:
    subject = f'{config.PROJECT_NAME} - Password recovery for email {email_to}'
    with open(f'{config.EMAIL_TEMPLATES_DIR}/reset_password.html', 'r', encoding='utf-8') as f:
        template_str = f.read()
    link = f'{config.FRONT_END_BASE_URL}/reset-password?token={token}'
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            'project_name': config.PROJECT_NAME,
            'email': email_to,
            'link': link,
            # dividing by 3600 to get the number of hours from the number of seconds
            'expire_hours': config.RESET_PASSWORD_TOKEN_LIFETIME_SECONDS / 3600,
        }
    )


def send_account_verification_email(*, email_to: str, token: str) -> None:
    subject = f'{config.PROJECT_NAME} - Account verification for email {email_to}'
    with open(f'{config.EMAIL_TEMPLATES_DIR}/account_verification.html', 'r', encoding='utf-8') as f:
        template_str = f.read()
    link = f'{config.FRONT_END_BASE_URL}/verify-account?token={token}'
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            'project_name': config.PROJECT_NAME,
            'email': email_to,
            'link': link,
            # dividing by 3600 to get the number of hours from the number of seconds
            'expire_hours': config.VERIFY_TOKEN_LIFETIME_SECONDS / 3600,
        }
    )
