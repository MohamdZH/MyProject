import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.0")
print("installed")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]


abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

web3 = Web3(Web3.HTTPProvider(os.getenv("Infura_EndPoint")))
chain_id = 4

address = "0x25E681EE76469E4cF846567b772e94e082907117"
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = web3.eth.contract(abi = abi,bytecode = bytecode)


nonce = web3.eth.getTransactionCount(address)
print(nonce)

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": web3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    }
)

signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract...")

tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

print("Waiting for transaction to finish...")

tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

#interacting with the deployed contract

simple_storage = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")
greeting_transaction = simple_storage.functions.store(4000).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": web3.eth.gas_price,
        "from": address,
        "nonce": nonce + 1,
    }
)
signed_greeting_txn = web3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)
tx_greeting_hash = web3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())
