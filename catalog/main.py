from fastapi import FastAPI
from starlette.requests import Request


app = FastAPI(
    title="Movie Catalog",
)

@app.get("/")
def read_root(request: Request):
    url_docs = request.url.replace(path="/docs", query="",)
    return {
        "massage": "Hello World",
        "url": str(url_docs),
    }
