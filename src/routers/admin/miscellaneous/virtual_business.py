
from fastapi import APIRouter, Depends

from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.admin.miscellaneous import virtual_business as data_access
from src.schemas.VirtualBusiness import AddVirtualBusinessRequest, GetVirtualBusinessRequest
from src.utilities.utils import data_frame_to_json_object

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/add_virtual_business', dependencies=[Depends(RightsChecker([38]))])
def add_virtual_business(req: AddVirtualBusinessRequest, token_payload:any = Depends(get_current_user)):
    by_admin_id = token_payload["user_id"]
    
    dataset = data_access.insert_virtual_business(req=req, admin_user_id=by_admin_id)
    if len(dataset)>0 and len(dataset['rs']):
        ds = dataset['rs']
        if(ds.iloc[0].loc["success"]):
            return {'success': True, 'message': ds.iloc[0].loc["message"] }
    
        return {'success': False, 'message': ds.iloc[0].loc["message"] }
    
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR }



@router.post('/get_virtual_business', dependencies=[Depends(RightsChecker([39]))])
def get_virtual_business(req: GetVirtualBusinessRequest, token_payload: any = Depends(get_current_user)):
    match_exact_user_id = False

    if(token_payload["role"]!="Admin"):
        match_exact_user_id = True

    dataset = data_access.get_virtual_business(req=req, match_exact_user_id=match_exact_user_id)
    if len(dataset)>0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}
    
    return {'success': False, 'message': DATABASE_CONNECTION_ERROR }



@router.get('/get_total_matching_business', dependencies=[Depends(RightsChecker([38]))])
def get_total_matching_business(user_id: str, binary_type_id: int):
    dataset = data_access.get_total_matching_business(user_id=user_id, binary_type_id=binary_type_id)
    if len(dataset) > 0:
        ds = dataset['rs']
        return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds)}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

