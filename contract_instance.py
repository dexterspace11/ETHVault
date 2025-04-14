import json
from web3 import Web3
from contract_config import RPC_URL, CONTRACT_ADDRESS

# Load ABI
with open("contract_abi.json") as f:
    contract_abi = json.load(f)

# Connect to Ethereum node
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Check connection
if web3.is_connected():
    print("✅ Connected to Ethereum network")
else:
    raise ConnectionError("❌ Could not connect to Ethereum network.")

# Load contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# Confirm functions available
print("✅ Contract loaded successfully. Available functions:")
for fn in contract.functions:
    print(f" - {fn.fn_name}")
