from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from config import VERSION
from src.infrastructure.logger.logger import Logger


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
