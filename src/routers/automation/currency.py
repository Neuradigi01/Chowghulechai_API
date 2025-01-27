import json

import requests
from fastapi import APIRouter

from src.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_AUTOMATION_KEY
from src.data_access.automation import currency as data_access
from src.utilities.utils import config

router = APIRouter()


@router.get('/fetch_currency_rates')
def fetch_currency_rates(key: str):
    if key == config['AutomationKey']:
        response = requests.get(config['CryptoPaymentGateway']['BaseURL'] + 'get_currencies_rates?'
                                'from_currency_symbols=USD,BTC,ETH,BNB,MATIC,TRX,USDT,USDC,AVAX,INR,LINK,DAI,AAVE,SAND,CRV,GNS,LDO'
                                '&to_currency_symbols=USD,BTC,ETH,BNB,MATIC,TRX,USDT,USDC,AVAX,INR,LINK,DAI,AAVE,SAND,CRV,GNS,LDO')

        crypto_data = response.json()

        dataset = data_access.update_currency_rates(_rates=json.dumps(crypto_data['data']))

        if len(dataset) > 0 and len(dataset['rs']) > 0:
            return {'success': True, 'message': dataset['rs'].iloc[0].loc['message']}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    return {'success': False, 'message': INVALID_AUTOMATION_KEY}

