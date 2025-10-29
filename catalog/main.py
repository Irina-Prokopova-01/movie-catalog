import logging

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

from api import router as api_router
from app_lifspan import lifespan
from core import config


logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)
app = FastAPI(
    title="Movie Catalog",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/")
def read_root(request: Request) -> dict[str, str]:
    url_docs = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "massage": "Hello World",
        "url": str(url_docs),
    }


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
