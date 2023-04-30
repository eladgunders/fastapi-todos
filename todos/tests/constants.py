from typing import Final

from pydantic import EmailStr

TEST_USER_EMAIL: Final[EmailStr] = EmailStr('test@test.com')
TEST_USER_PASSWORD: Final[str] = 'test'
TEST_BASE_URL: Final[str] = 'http://test'
INITIAL_DATA_FILE_PATH: Final[str] = 'todos/scripts/initial_data.json'
