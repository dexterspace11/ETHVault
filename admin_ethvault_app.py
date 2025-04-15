import streamlit as st
from web3 import Web3
import json
from eth_account import Account

# --- Configuration ---
st.set_page_config(page_title="ETH Vault Admin", layout="centered")
st.title("🛠️ ETH Vault Admin Panel")

# Load ABI and Bytecode
with open("contract_abi.json") as f:
    contract_abi = json.load(f)

with open("contract_bytecode.json") as f:
    bytecode_data = json.load(f)
    contract_bytecode = bytecode_data["bytecode"]

# Connect to Ethereum
rpc_url = st.text_input("RPC URL (e.g., https://sepolia.infura.io/v3/YOUR_PROJECT_ID):", type="password")
private_key = st.text_input("Enter Admin Private Key:", type="password")

if rpc_url and private_key:
    try:
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        account = Account.from_key(private_key)
        st.success(f"Connected as: {account.address}")
        web3.eth.default_account = account.address

        # Deploy Button
        if st.button("🚀 Deploy Vault Contract"):
            contract = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
            nonce = web3.eth.get_transaction_count(account.address)
            tx = contract.constructor().build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': web3.to_wei('10', 'gwei')
            })

            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            st.info("⏳ Waiting for transaction confirmation...")
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            contract_address = tx_receipt.contractAddress
            st.success(f"✅ Contract Deployed at: {contract_address}")

            # Save deployed address to session
            st.session_state["contract_address"] = contract_address

    except Exception as e:
        st.error(f"❌ Error during connection or deployment: {str(e)}")

# Optional: Interact with deployed contract
st.markdown("---")
st.subheader("🔍 Manage Existing Vault")

contract_address_input = st.text_input("Enter Vault Contract Address:")
contract_address = st.session_state.get("contract_address", contract_address_input)

if contract_address and web3.is_address(contract_address):
    try:
        contract_instance = web3.eth.contract(address=contract_address, abi=contract_abi)

        if st.button("📊 View Total ETH in Vault"):
            total_eth = contract_instance.functions.getTotalETH().call()
            st.success(f"Total ETH in Vault: {web3.from_wei(total_eth, 'ether')} ETH")

        if st.button("⚙️ Trigger Auto-Compounding for All"):
            tx = contract_instance.functions.autoCompoundAll().build_transaction({
                'from': account.address,
                'nonce': web3.eth.get_transaction_count(account.address),
                'gas': 1500000,
                'gasPrice': web3.to_wei('10', 'gwei')
            })
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            st.success(f"Auto-compounding triggered! TX Hash: {tx_hash.hex()}")

    except Exception as e:
        st.error(f"❌ Error interacting with contract: {str(e)}")
