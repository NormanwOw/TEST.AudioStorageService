from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from config import VERSION
from src.infrastructure.logger.logger import Logger
from src.presentation.routers.auth_routers.router import router as auth_router
from src.presentation.routers.user_routers.router import router as user_router
from src.presentation.routers.file_routers.router import router as file_router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncIterator[None]:
    logger = Logger()
    logger.info('Start app...')
    yield
    logger.info('App shutdown')

app = FastAPI(
    title='Audio Storage Service',
    version='1.0.0',
    docs_url=f'/api/v{VERSION}/docs',
    openapi_url=f'/api/v{VERSION}/openapi.json',
    redoc_url=None,
    lifespan=lifespan
)

app.include_router(
    auth_router
)
app.include_router(
    user_router
)
app.include_router(
    file_router
)
