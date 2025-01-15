from fastapi import APIRouter, Depends

from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.team import matrix as data_access
from src.schemas.TeamDetails import GetMatrixMembers
from src.utilities.utils import data_frame_to_json_object

router = APIRouter(
    tags=["Matrix"]
)


@router.get('/get_pools', dependencies=[Depends(RightsChecker([152, 153, 154, 155, 156, 157, 158, 159])), Depends(get_current_user)])
def get_pools():
    dataset = data_access.get_pools()
    if len(dataset) > 0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

@router.get('/get_pool_entry_ids', dependencies=[Depends(RightsChecker([152, 153, 154, 155, 156, 157, 158, 159])), Depends(get_current_user)])
def get_pool_entry_ids(user_id: str, pool_id: int):
    dataset = data_access.get_pool_entry_ids(user_id=user_id, pool_id=pool_id)
    if len(dataset) > 0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


@router.post('/get_matrix_members', dependencies=[Depends(RightsChecker([152, 153, 154, 155, 156, 157, 158, 159])), Depends(get_current_user)])
def get_matrix_members(req: GetMatrixMembers, token_payload: any = Depends(get_current_user)):
    if(token_payload["role"]!='Admin'):
        req.user_id = token_payload["user_id"]

    dataset = data_access.get_matrix_members(req)
    if len(dataset) > 0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds),
                'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}


