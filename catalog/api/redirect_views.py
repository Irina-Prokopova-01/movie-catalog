from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.responses import RedirectResponse

from api.api_v1.mouvie_a.dependencies import read_movie
from schemas.movie import Movie

router = APIRouter(
    prefix="/r",
    tags=["Redirect"],
)


@router.get("/{slug}/")
@router.get("/{slug}")
def redirect_movie(
    url: Annotated[
        Movie,
        Depends(read_movie),
    ],
) -> RedirectResponse:
    return RedirectResponse(
        url=str(url.title),
    )
