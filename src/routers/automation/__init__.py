
from fastapi import APIRouter

from .arbitrage_trade_transactions import router as arbitrage_trade_transactions_router
from .currency import router as currency_router

router = APIRouter(
    prefix="/automation",
    tags=["Automation"]
)

router.include_router(currency_router)
router.include_router(arbitrage_trade_transactions_router)
