from decimal import Decimal

import requests

from src.utilities.utils import config


def get_token_rate(base_token_symbol: str, quote_token_symbol: str) -> Decimal:
    if base_token_symbol not in [''] and quote_token_symbol not in ['']:
        response = requests.get(config['CryptoPaymentGateway']['BaseURL'] + 'get_currencies_rates?from_currency_symbols=' + base_token_symbol + '&to_currency_symbols='+quote_token_symbol)

        crypto_data = response.json()
        rate = crypto_data['data'][base_token_symbol][quote_token_symbol]
        print(rate)
        return Decimal(rate)