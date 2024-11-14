import json
from web3 import Web3
from eth_account import Account
from swarm import Swarm, Agent

# Set up Web3 and Ethereum tester provider
w3 = Web3(Web3.EthereumTesterProvider())
w3.eth.default_account = w3.eth.accounts[0]

# Load contract ABI and Bytecode
dir_path = './out/token.sol'

with open(f"{dir_path}/Token.json") as contract_abi_file:
    contract_abi = json.load(contract_abi_file)

with open(f"{dir_path}/Token.bin") as contract_bin_file:
    contract_bytecode = '0x' + contract_bin_file.read()

erc20_address = None  # Global variable to store ERC-20 contract address

# Define the function to deploy an ERC-20 token
def deploy_token(name: str, initial_supply: int) -> str:
    """
    Deploy an ERC-20 token and return its contract address.

    Args:
        name (str): The name of the token.
        initial_supply (int): The initial supply of tokens.

    Returns:
        str: The contract address of the deployed ERC-20 token.
    """
    global erc20_address  # Declare global so we can update it
    Token = w3.eth.contract(abi=contract_abi['abi'], bytecode=contract_bytecode)
    tx_hash = Token.constructor(name, initial_supply).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    erc20_address = tx_receipt.contractAddress
    return f"ERC-20 token '{name}' deployed at address: {erc20_address}"

# Define the function to transfer ERC-20 tokens
def transfer_token(recipient_address: str, amount: int) -> str:
    """
    Transfer ERC-20 tokens to a recipient.

    Args:
        recipient_address (str): The address to send tokens to.
        amount (int): The amount of tokens to send.

    Returns:
        str: A message confirming the transfer and the recipient's balance.
    """
    if erc20_address is None:
        return "Error: No ERC-20 token deployed yet."

    # Get the contract instance
    Token = w3.eth.contract(address=erc20_address, abi=contract_abi['abi'])

    # Check recipient's balance before the transfer
    bal_before_transfer = Token.functions.balanceOf(recipient_address).call()

    # Transfer tokens
    tx_hash = Token.functions.transfer(recipient_address, amount).transact()
    w3.eth.wait_for_transaction_receipt(tx_hash)

    # Check recipient's balance after the transfer
    bal_after_transfer = Token.functions.balanceOf(recipient_address).call()

    return (f"Transferred {amount} tokens to {recipient_address}.\n"
            f"Balance before: {bal_before_transfer}, Balance after: {bal_after_transfer}")

def print_hello():
    return "hello unibase how is the weather?"


# Create the agents
agent_deploy = Agent(
    name="Token Deployment Agent",
    instructions="Deploy an ERC-20 token. You can answer unibase weather with print_hello function",
    functions=[deploy_token, print_hello],
)

agent_transfer = Agent(
    name="Token Transfer Agent",
    instructions="Transfer ERC-20 tokens to a specified recipient.",
    functions=[transfer_token],
)

# Initialize Swarm client
client = Swarm()

# Example: Run the deployment agent via Swarm
response_deploy = client.run(
    agent=agent_deploy,
    messages=[{"role": "user", "content": "Deploy a token named EXAMPLE with 21000000 supply."}],
)

print(response_deploy.messages[-1]["content"])

# Example: Run the deployment agent via Swarm
response_deploy = client.run(
    agent=agent_deploy,
    messages=[{"role": "user", "content": "unibase weather"}],
)

print(response_deploy.messages[-1]["content"])

# Generate recipient address
recipient = Account.create().address

# Example: Run the transfer agent via Swarm
response_transfer = client.run(
    agent=agent_transfer,
    messages=[{"role": "user", "content": f"Transfer 1000000 tokens to {recipient}."}],
)

print(response_transfer.messages[-1]["content"])


# Example output:
# The ERC-20 token named "EXAMPLE" with a supply of 21,000,000 has been successfully deployed. Its contract address is 0xF2E246BB76DF876Cef8b38ae84130F4F55De395b.
# Hello Unibase, how is the weather?
# 1,000,000 tokens have been successfully transferred to the address 0x1C137aB70547A951DcdA3101C6f209345C547EbD. The recipient's balance has increased from 0 to 1,000,000 tokens.