import logging

from fastapi import FastAPI, HTTPException, status
from starlette.requests import Request

from api import router as api_router
from core import config


logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)
app = FastAPI(
    title="Movie Catalog",
)

app.include_router(api_router)


@app.get("/")
def read_root(request: Request):
    url_docs = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "massage": "Hello World",
        "url": str(url_docs),
    }
