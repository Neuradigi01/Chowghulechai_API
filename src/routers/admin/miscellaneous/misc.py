from fastapi import APIRouter, Depends

from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.constants.messages import DATABASE_CONNECTION_ERROR
from src.data_access.admin.miscellaneous import misc as data_access

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/update_roi_percentage', dependencies=[Depends(RightsChecker([242]))])
def update_roi_percentage(package_id: int, roi_percentage: float, token_payload: any = Depends(get_current_user)):
    by_admin_id = token_payload["user_id"]

    dataset = data_access.update_roi_percentage(package_id=package_id, roi_percentage=roi_percentage, admin_user_id=by_admin_id)
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["success"]:
            return {'success': True, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
