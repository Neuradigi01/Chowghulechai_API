
from fastapi import APIRouter, Depends

from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.data_access.income import referral as data_access
from src.schemas.Income import GetReferralIncome_Request
from src.utilities.utils import data_frame_to_json_object

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post('/get_referral_income', dependencies=[Depends(RightsChecker([134, 135]))])
def get_referral_income(req: GetReferralIncome_Request, token_payload: any = Depends(get_current_user)):
    match_exact_user_id = False
    if(token_payload["role"]=='User'):
        req.user_id = token_payload["user_id"]
        match_exact_user_id = True
        
    dataset = data_access.get_referral_income(req=req, match_exact_user_id=match_exact_user_id)
    # print(dataset)
    if len(dataset) > 0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}
        
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

