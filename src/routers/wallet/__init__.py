
from fastapi import APIRouter

from .credit_request import router as credit_request_router
from .fund_transfer import router as fund_transfer_router
from .wallet import router as wallet_router

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)

router.include_router(wallet_router)
router.include_router(fund_transfer_router)
router.include_router(credit_request_router)