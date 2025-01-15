
from fastapi import APIRouter, Request, Depends

from src.business_layer import login_service
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.schemas.Accounts import LoginRequest

router = APIRouter(
    tags=["Login"]
)


@router.post('/login')
def login(data: LoginRequest, request: Request):
    return login_service.login(username=data.username, password=data.password, request=request)


@router.post('/login_through_admin', dependencies=[Depends(RightsChecker([26]))])
def login(data: LoginRequest, request: Request, token_payload: any = Depends(get_current_user)):
    return login_service.login(username=data.username, password=data.password, request=request, by_admin_user_id=token_payload['user_id'])
