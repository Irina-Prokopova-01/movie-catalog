__all__ = "router"

from .detail_views import router as detail_router
from .views_list import router

router.include_router(detail_router)
