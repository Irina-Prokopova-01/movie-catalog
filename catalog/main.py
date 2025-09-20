from fastapi import FastAPI, HTTPException, status
from starlette.requests import Request
from schemas.movie import Movie

from api import router as api_router

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
