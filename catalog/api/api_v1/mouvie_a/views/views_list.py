from fastapi import APIRouter, status, BackgroundTasks

from api.api_v1.mouvie_a.crud import storage
from schemas.movie import BaseMovie, CreateMovie, MovieRead

router = APIRouter(
    prefix="/movies",
    tags=["Movies_list"],
)


@router.get("/list_movies/", response_model=list[MovieRead])
def list_all_movies() -> list[BaseMovie]:
    return storage.get()


@router.post(
    "/create_movie/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie_create_new: CreateMovie,
    background_tasks: BackgroundTasks,
) -> BaseMovie:
    background_tasks.add_task(storage.save_state)
    return storage.create(movie_create_new)
