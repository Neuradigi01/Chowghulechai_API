from fastapi import APIRouter
from .image_upload import router  as imge_upload

router = APIRouter(
    prefix="/ads",
    tags=["ADS"]
)

router.include_router(imge_upload)
