import logging

import uvicorn
from api import router as api_router
from api.main_views import router as main_router
from app_lifspan import lifespan
from core import config
from fastapi import FastAPI
from starlette.requests import Request

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)
app = FastAPI(
    title="Movie Catalog",
    lifespan=lifespan,
)

app.include_router(api_router)
app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
