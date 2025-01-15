
from fastapi import APIRouter

from src.constants.messages import (DATABASE_CONNECTION_ERROR)
from src.data_access.setup import routes as data_access
from src.schemas.Setup import AddRoute, UpdateActiveRoutes
from src.utilities.helper_utils import generate_routes_json

router = APIRouter()


@router.post('/add_edit_route')
async def add_edit_route(req: AddRoute):
    dataset = data_access.add_edit_route(req=req)
    # print(dataset)
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["success"]:
            generate_routes_json()
            return {'success': True, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}



@router.delete('/delete_route')
async def delete_route(id: int):
    dataset = data_access.delete_route(id=id)
    # print(dataset)
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["success"]:
            generate_routes_json()
            return {'success': True, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}



@router.put('/update_active_routes')
async def update_active_routes(req: UpdateActiveRoutes):
    dataset = data_access.update_active_routes(user_type=req.user_type, route_ids=req.route_ids)
    # print(dataset)
    if len(dataset) > 0 and len(dataset['rs']):
        ds = dataset['rs']
        if ds.iloc[0].loc["success"]:
            generate_routes_json()
            return {'success': True, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': ds.iloc[0].loc["message"]}

    return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
