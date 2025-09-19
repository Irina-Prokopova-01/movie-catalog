from fastapi import FastAPI, HTTPException, status
from starlette.requests import Request
from schemas.movie import Movie


app = FastAPI(
    title="Movie Catalog",
)


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


LIST_MOVIES = [
    Movie(
        movie_id=1,
        title="Movie 1",
        description="Movie description1",
        year=2020,
        rating=4.5,
    ),
    Movie(
        movie_id=2,
        title="Movie 2",
        description="Movie description2",
        year=2025,
        rating=4.7,
    ),
    Movie(
        movie_id=3,
        title="Movie 3",
        description="Movie description3",
        year=2025,
        rating=4.8,
    ),
]


@app.get("/list_movies/", response_model=list[Movie])
def list_all_movies():
    return LIST_MOVIES


@app.get("/{movie_id}", response_model=Movie)
def read_movie(movie_id: int):
    for movie in LIST_MOVIES:
        if movie.movie_id == movie_id:
            return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {movie_id!r} not found.",
    )
