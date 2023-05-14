import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.core.config import get_config

config = get_config()

app = FastAPI(
    title=config.PROJECT_NAME,
    openapi_url=f'{config.API_V1_STR}/openapi.json'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app)
