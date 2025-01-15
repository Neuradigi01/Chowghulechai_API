import requests
from fastapi import APIRouter

from src.business_layer.dapp_service import process_dapp_contract_transaction
from src.constants.messages import INVALID_AUTOMATION_KEY
from src.utilities.utils import config

router = APIRouter()


@router.get('/fetch_dapp_contract_transactions')
def fetch_dapp_contract_transactions(key: str):
    if key == config['AutomationKey']:
        dapp_config = config['DApp']

        url = (dapp_config["ExplorerApiUrl"]+"?module=account&action=txlist&address="
                + dapp_config['ContractAddress']
                + "&startblock="+str(dapp_config['StartBlock'])
                + "&endblock=99999999&page=1&offset=10&sort=desc&apikey="
                + dapp_config['ExplorerApiKey'])

        response = requests.request('GET', url=url)
        data = response.json()

        for transaction in data['result']:
            process_dapp_contract_transaction(txn_hash=transaction['hash'])

        return {'success': False, 'message': 'Transactions saved successfully!'}
    return {'success': False, 'message': INVALID_AUTOMATION_KEY}

