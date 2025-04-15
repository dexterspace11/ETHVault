from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

RPC_URL = f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

CONTRACT_ADDRESS = "0xYourVaultContract"
with open("contract_abi.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
