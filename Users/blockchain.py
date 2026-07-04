from web3 import Web3
import json
import os

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load contract
contract_address = "0xFcE37df41A7d074E98D17C87AFe491b08D75ee5B"
abi_path = os.path.join(os.path.dirname(__file__), 'KYC_ABI.json')

with open(abi_path) as f:
    abi = json.load(f)

contract = web3.eth.contract(address=contract_address, abi=abi)

default_account = web3.eth.accounts[0]
web3.eth.default_account = default_account

def get_customer_from_blockchain(national_id):
    try:
        result = contract.functions.getCustomer(national_id).call()
        return {
            'full_name': result[0],
            'national_id': result[1],
            'kyc_status': result[2],
            'added_by_bank': result[3]
        }
    except Exception as e:
        print("Error reading from blockchain:", e)
        return None
