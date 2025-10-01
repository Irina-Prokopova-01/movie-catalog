from fastapi import APIRouter
from api.api_v1.mouvie_a.views import router as views_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(views_router)
