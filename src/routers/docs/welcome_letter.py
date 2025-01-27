
import pdfkit
import pystache
from fastapi import APIRouter, Depends, Response

from src.business_layer.security.Jwt import get_current_user
from src.business_layer.security.RightsChecker import RightsChecker
from src.data_access.user import details as user_details_data_access
from src.utilities.helper_utils import company_dict
from src.utilities.utils import getPdfKitConfig, convert_timestamp_to_datetime_with_timezone

router = APIRouter(dependencies=[Depends(get_current_user)])
 
@router.get('/get_welcome_letter', dependencies=[Depends(RightsChecker([116]))])
def get_welcome_letter(user_id: str):
    pdf_bytes = get_welcome_letter_pdf_bytes(user_id=user_id)
    response = Response(content=pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=welcome.pdf"
    return response
        

@router.get('/get_welcome_letter_html', dependencies=[Depends(RightsChecker([116]))])
def get_welcome_letter_html(user_id: str):
    dataset = user_details_data_access.get_user_details(user_id=user_id)
    # print(dataFrameToJsonObject(dataset['rs']))
    df = dataset['rs']
    row = df.iloc[0]
    with open('templates/docs/welcome_letter.html', 'r') as file:
        template = file.read()
        a = {
                'user_id':row['user_id'],
                'user_name':row['name'],
                'joining_date':convert_timestamp_to_datetime_with_timezone(row['joining_date']),
                'sponsor_id':row['sponsor_id'],
                'joining_amount':round(row['joining_amount'], int(company_dict['round_off_digits']))
            }

        c = a | company_dict

        template = pystache.render(template, c)

        return template



def get_welcome_letter_pdf_bytes(user_id: str):
    html = get_welcome_letter_html(user_id=user_id)
    config = getPdfKitConfig()
    pdf_bytes = pdfkit.from_string(html, False, configuration=config)
    return pdf_bytes

