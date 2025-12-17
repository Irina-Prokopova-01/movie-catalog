from datetime import date, datetime

from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from core.config import BASE_DIR

def jinja_context(
    request: Request,
)-> dict[str, date]:
    return {
        "today": date.today(),
        "now": datetime.now(),

    }

templates = Jinja2Templates(
    directory=BASE_DIR / "templates",
    context_processors=[jinja_context],
)