from app.api.auth import fast_api_users

current_logged_user = fast_api_users.current_user(active=True, verified=False, superuser=False)
