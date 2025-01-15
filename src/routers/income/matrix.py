from fastapi import APIRouter, Depends

from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.data_access.income import matrix as data_access
from src.schemas.Income import GetMatrixIncome_Request
from src.utilities.utils import data_frame_to_json_object

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post('/get_matrix_income', dependencies=[Depends(RightsChecker([136, 137, 138, 139]))])
def get_matrix_income(req: GetMatrixIncome_Request, token_payload: any = Depends(get_current_user)):
    if (token_payload["role"] == 'User'):
        req.user_id = token_payload["user_id"]
        req.match_exact_user_id = True

    dataset = data_access.get_matrix_income(req=req, match_exact_user_id=req.match_exact_user_id)
    # print(dataset)
    if len(dataset) > 0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds),
                'settings': data_frame_to_json_object(dataset['rs1'])}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}



@router.get('/get_matrix_income_concise', dependencies=[Depends(RightsChecker([138, 139]))])
def get_matrix_income_concise(user_id: str, pool_id: int, matrix_id: int, token_payload: any = Depends(get_current_user)):
    if (token_payload["role"] == 'User'):
        user_id = token_payload["user_id"]

    dataset = data_access.get_matrix_income_concise(user_id=user_id, pool_id=pool_id, matrix_id=matrix_id)
    # print(dataset)
    if len(dataset) > 0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds),
                'settings': data_frame_to_json_object(dataset['rs1'])}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

