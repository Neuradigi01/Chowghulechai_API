# from cmath import e
from fastapi import APIRouter, Depends
from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.constants.messages import OK, DATABASE_CONNECTION_ERROR
from src.data_access.ads import image_upload  as data_access
from src.utilities.utils import  data_frame_to_json_object, save_base64_file
from src.schemas.image_upload import ImageUpload, GetAdsDetail,AdsApproveByAdmin

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post('/image_upload')
async def image_upload(req: ImageUpload , token_payload: any = Depends(get_current_user)):

    try:
        if req.image == '':
            return {'success': False, 'message': 'Upload at least one image for the Ads'}

        image_name = ''

        if req.image != '':
            image_name, path = save_base64_file(req.image, upload_file_name='Ad')


        dataset =  data_access.images_upload(image = image_name, user_id= token_payload["user_id"], user_type =  token_payload["role"] )   

        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return{'success': False, 'message': 'An error occurred'}
        

@router.post('/get_ads_details')
def get_ads_details(req : GetAdsDetail, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if(token_payload["role"]=='User'):
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True 

        dataset =  data_access.GetAdsDetail(req=req , match_exact_user_id= match_exact_user_id)   
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': data_frame_to_json_object(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}
        
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return{"seucces" :False, 'message': 'An error occured'}


@router.post('/ads_approved')
def ads_approved_by_admin(req : AdsApproveByAdmin , token_payload: any = Depends(get_current_user)):
    try:
        # user_id = token_payload["user_id"]
        admin_id = token_payload["user_id"]

        dataset = data_access.AdsApprovedByAdmin( admin_id= admin_id , ad_id=req.ad_id , status=req.status )

        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
        
    except Exception as e:
        print(e.__str__())
        return{"seucces" :False, 'message': 'An error occured'}