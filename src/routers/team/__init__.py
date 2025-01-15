
from fastapi import APIRouter

from .matrix import router as matrix
from .team import router as team
from .tree import router as tree

router = APIRouter(
    prefix="/team_details"
)

router.include_router(team)
router.include_router(tree)
router.include_router(matrix)