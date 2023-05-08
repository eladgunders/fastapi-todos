from urllib.request import Request

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse

from app.api import router
from app.core.config import get_config

config = get_config()

app = FastAPI(
    title='TODOS API',
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


# override the default fastapi HTTP status code (422) with 400 to mark it as a client bad request
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({'detail': exc.errors(), 'body': exc.body}),
    )

if __name__ == '__main__':
    uvicorn.run(app)
