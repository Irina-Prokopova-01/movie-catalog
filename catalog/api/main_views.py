from datetime import date
from fastapi import (
    APIRouter,
    Request,
)
from starlette.responses import HTMLResponse

from core.config import BASE_DIR
from templating import templates

router = APIRouter(
    tags=["Read Root"],
)


@router.get(
    "/",
    response_class=HTMLResponse,
    # include_in_schema=False,
)
def read_root(
    request: Request,
) -> HTMLResponse:
    context = {}
    today = date.today()
    features = [
        "Create short URLs",
        "Track all redirects",
        "Real-time statistics",
        "Shared management",
    ]
    context.update(
        today=today,
        features=features,
    )
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )
