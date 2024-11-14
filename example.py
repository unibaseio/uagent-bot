import json
from web3 import Web3
from eth_account import Account

# Deploy Erc20
dir_path = './out/token.sol'
with open(f"{dir_path}/Token.json") as contract_abi_file:
    contract_abi = json.load(contract_abi_file)

with open(f"{dir_path}/Token.bin") as contract_bin_file:
    contract_bytecode = '0x' + contract_bin_file.read()

w3 = Web3(Web3.EthereumTesterProvider())
w3.eth.default_account = w3.eth.accounts[0]

Token = w3.eth.contract(abi=contract_abi['abi'], bytecode=contract_bytecode)
tx_hash = Token.constructor("EXAMPLE", 21000000).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
erc20_address = tx_receipt.contractAddress
print(f"Erc20 address: {erc20_address}")


# Transfer Erc20
Token = w3.eth.contract(address=erc20_address, abi=contract_abi['abi'])
recipient = Account.create().address
bal_before_transfer = Token.functions.balanceOf(recipient).call()
print(f"Recipient: {recipient}, Balance: {bal_before_transfer}")

tx_hash = Token.functions.transfer(recipient, 1000000).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

bal_after_transfer = Token.functions.balanceOf(recipient).call()
print(f"Recipient: {recipient}, Balance: {bal_after_transfer}")

# Output:
#
# Erc20 address: 0xF2E246BB76DF876Cef8b38ae84130F4F55De395b
# Recipient: 0xa78043548c687790f1023095bA0394A86AfE985c, Balance: 0
# Recipient: 0xa78043548c687790f1023095bA0394A86AfE985c, Balance: 1000000
