from fastapi_users.authentication import AuthenticationBackend, BearerTransport

from app.users.security import get_jwt_strategy


bearer_transport = BearerTransport(tokenUrl='auth/login')

auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
