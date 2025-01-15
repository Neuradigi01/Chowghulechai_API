from pydantic import BaseModel




class ImageUpload(BaseModel):
    image : str = ''
 

class GetAdsDetail(BaseModel):
    user_id: str =''
    date_from: str = ''
    date_to: str = ''
    page_index: int = 0
    page_size: int = 100
    
class AdsApproveByAdmin(BaseModel):
    ad_id : int
    status : str