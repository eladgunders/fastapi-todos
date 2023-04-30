from typing import Final

from pydantic import EmailStr

TEST_USER_EMAIL: Final[EmailStr] = EmailStr('test@test.com')
TEST_USER_PASSWORD: Final[str] = 'test'
