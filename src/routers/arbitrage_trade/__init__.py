
from fastapi import APIRouter

from .details import router as details_router
from .trade import router as trade_router

router = APIRouter(
    prefix="/arbitrage",
    tags=["Arbitrage Trade"]
)

router.include_router(trade_router)
router.include_router(details_router)
