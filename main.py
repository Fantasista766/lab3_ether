from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account
import json
import os


"""config"""
owner_private_key_dir = '.env'
load_dotenv(owner_private_key_dir)
sepolia_url = 'https://rpc.sepolia.org'
w3 = Web3(Web3.HTTPProvider(sepolia_url))

token_address = '0xEB6Fa24e991bd840b22D7fCf0c2dd832968FDFb9'
owner_private_key = os.environ.get('PRIVATE_KEY')
owner = Account.from_key(owner_private_key)
owner_address = owner.address

# а) создание экземпляра СмК
abi_dir = 'NesToken_metadata.json'
abi_data = json.loads(open(abi_dir).read())['output']['abi']
token_contract = w3.eth.contract(address=token_address, abi=abi_data)  # работает
functions_pool = token_contract.functions


def get_balances(pre_string=''):
    """Печатает текущие балансы участников"""
    print(pre_string)
    print('Balances (in tokens):')
    print('Total supply:', functions_pool.totalSupply().call())
    print(f'Owner Balance:', functions_pool.balanceOf(owner_address).call())
    print(f'Contract balance:', functions_pool.balanceOf(token_address).call())
    print()


def transfer():
    """Выполняет вызов функции токена transfer"""
    print('Transfer function')
    transaction = functions_pool.transfer(token_address, 1000).build_transaction({
        'gas': 100000,
        'gasPrice': w3.to_wei('1', 'gwei'),
        'from': owner_address,
        'nonce': w3.eth.get_transaction_count(owner_address)
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=owner_private_key)
    send_tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    print(tx_receipt)


def check_event():
    """Получает событие, порождённое функцией transfer"""
    print('EVENT IN MAIN file')
    logs = token_contract.events.Transfer().get_logs(fromBlock=w3.eth.block_number)
    print(logs)


def main():
    get_balances()  # б) вызов функции через call
    transfer()  # б) вызов функции через транзакцию
    check_event()  # в) получение события по СмК
    get_balances()


if __name__ == '__main__':
    main()
