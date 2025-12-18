from typing import Annotated

from fastapi.params import Depends

from core.config import settings
from storage.movie_a import Storage


def get_movie_storage()->Storage:
    return Storage(
        hash_name=settings.redis.collection_names.movie_hash_name
    )

GetMovieStorage = Annotated[
    Storage,
    Depends(get_movie_storage)
]