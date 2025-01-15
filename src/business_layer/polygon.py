from decimal import Decimal

from eth_account import Account
from web3 import Web3, HTTPProvider
import requests
from web3.middleware import geth_poa_middleware

from src.constants.messages import OK
from src.utilities.aes import aes
from src.utilities.utils import log_error, amount_in_smallest_unit

network = "Polygon"
polygon_chain_id = 137
api_keys = [
    {"key": 'INU1QKCGBX3EMPEW8FIZ7BNWB5KYDBVU8H', 'used_count': 0},
    {"key": 'C22W9MVGWBH2KKJE64ITR7ZKJBWVJSM36V', 'used_count': 0}
]
provider_url = 'https://rpc-mainnet.matic.quiknode.pro'
req_gas_to_send_token = 84000


def send_matic(from_private_key: str, to_address: str, amount: Decimal, max_fee: Decimal = None):
    try:
        w3 = Web3(Web3.HTTPProvider(provider_url))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not w3.is_connected():
            print("Failed to connect to the network")
            return

        # Set up the transaction details
        from_address = w3.eth.account.from_key(from_private_key).address
        nonce = w3.eth.get_transaction_count(from_address)
        value = w3.to_wei(amount, 'ether')  # Convert amount to Wei
        gas_price = w3.eth.gas_price*10
        gas_limit = 21000  # Standard gas limit for transaction

        if max_fee is not None and max_fee > 0:
            fee = Decimal(w3.from_wei(gas_price*gas_limit, 'ether'))
            if fee > max_fee:
                return {'success': False, 'message': 'Fee is too high!'}

        balance_eth = w3.from_wei(w3.eth.get_balance(from_address), 'ether')
        if Decimal(balance_eth) < (amount+(max_fee if max_fee is not None and max_fee > 0 else 0)):
            return {'success': False, 'message': 'Network congestion is high. Please try again later!'}

        # Construct the transaction
        txn = {
            'nonce': nonce,
            'chainId': polygon_chain_id,
            'to': Web3.to_checksum_address(to_address),
            'value': value,
            'gas': gas_limit,
            'gasPrice': gas_price,
        }

        # print(w3.eth.estimate_gas(transaction=txn))

        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=from_private_key)

        # Send the transaction
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash, timeout=1000)

        # print(f"Transaction sent! Hash: {txn_hash.hex()}")
        return {'success': True, 'message': OK, 'data': {'transaction_hash': txn_hash.hex(), 'success_status': txn_receipt['status']==1} }

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': log_error(e, extra_info='polygon: send_matic', extra_data='To: '+str(to_address)+', Amount: '+str(amount))}
