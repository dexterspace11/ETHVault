from dotenv import load_dotenv
import os

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID")

RPC_URL = f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}"
CONTRACT_ADDRESS = "0x7A690D391dAD281C3D4F2190Ec323244940da11b"



