import requests
from fastapi import APIRouter

from src.business_layer import arbitrage_service
from src.constants.messages import INVALID_AUTOMATION_KEY
from src.utilities.utils import config

router = APIRouter()


@router.get('/fetch_arbitrage_contract_transactions')
def fetch_arbitrage_contract_transactions(key: str):
    if key == config['AutomationKey']:
        arbitrage_config = config['ArbitrageTrade']

        url = ("https://api.polygonscan.com/api?module=account&action=txlist&address="
                + arbitrage_config['ContractAddress']
                + "&startblock="+str(arbitrage_config['StartBlock'])
                + "&endblock=99999999&page=1&offset=10&sort=desc&apikey="
                + config['PolygonScan']['ApiKey'])

        response = requests.request('GET', url=url)
        data = response.json()

        for transaction in data['result']:
            if transaction['methodId'] == "0xaf89f091":
                input_data = transaction['input']
                request_id = arbitrage_service.decode_input_data_for_request_id(input_data=input_data)

                if transaction['txreceipt_status'] == "1" and transaction['isError'] == "0":
                    arbitrage_service.update_trade_transaction_status(request_id=request_id, txn_hash=transaction['hash'], status='Success')
                else:
                    arbitrage_service.update_trade_transaction_status(request_id=request_id, txn_hash=transaction['hash'], status='Failed')

        return {'success': False, 'message': 'Transactions saved successfully!'}
    return {'success': False, 'message': INVALID_AUTOMATION_KEY}
    
