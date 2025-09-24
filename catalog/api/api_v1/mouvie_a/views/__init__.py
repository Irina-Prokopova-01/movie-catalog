__all__ = "router"

from .views_list import router
from .detail_views import router as detail_router


router.include_router(detail_router)
