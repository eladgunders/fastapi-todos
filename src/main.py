from urllib.request import Request
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse

from app import db
from app.api import router
from app.core.config import get_config

config = get_config()

app = FastAPI(title='TODOS API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event('startup')
def startup():
    db.connect_to_databases()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect_from_databases()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

if __name__ == '__main__':
    uvicorn.run(app)
