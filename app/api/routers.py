from fastapi import APIRouter

from app.api.ping import ping_router
from app.api.tender_views import tender_router
from app.api.bid_views import bid_router


main_router = APIRouter()
main_router.include_router(ping_router)
main_router.include_router(tender_router)
main_router.include_router(bid_router)
