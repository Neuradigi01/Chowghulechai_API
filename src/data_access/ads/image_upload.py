
from src.schemas.image_upload import ImageUpload , GetAdsDetail


from src.utilities.utils import execute_query

def images_upload(image: str, user_type : str , user_id : str):
    res = execute_query("call usp_image_upload( _image => %s, _user_type => %s, _user_id => %s)",(image, user_type, user_id ))
    return res

def GetAdsDetail(req : GetAdsDetail, match_exact_user_id : bool = False ):
    res = execute_query("call usp_get_ads_details(_user_id => %s , _match_exact_user_id => %s, _on_date => %s::timestamptz[], _page_index =>%s, _page_size => %s )" ,
                        (req.user_id, match_exact_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.page_index, req.page_size))
    return res

def AdsApprovedByAdmin(admin_id : str, ad_id: int ,status : str):
    res = execute_query( "call usp_ads_approved_by_admin (_admin_id =>%s , ad_id => %s, _status =>%s)",
                        (admin_id,ad_id,status))
    return res