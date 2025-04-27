# app_user.py

import streamlit as st
from web3 import Web3
import json

# ----------------------------
# Streamlit UI - Title
# ----------------------------
st.set_page_config(page_title="ETH Vault", page_icon="🔒")
st.title("🔒 ETH Vault - User Panel")

# ----------------------------
# Connect Wallet Section
# ----------------------------
st.sidebar.header("Wallet Connection")

private_key = st.sidebar.text_input("🔑 Enter Your Private Key", type="password")
vault_address = st.sidebar.text_input("🏦 Enter Vault Contract Address")

user_address = ""
vault = None

if private_key and vault_address:
    # Connect to Blockchain
    RPC_URL = "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # <--- Replace with your Infura Project ID
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    # Load ABI
    with open('vaultabi.json', 'r') as abi_file:
        vault_abi = json.load(abi_file)
    
    # Load Vault Contract
    vault = web3.eth.contract(address=Web3.to_checksum_address(vault_address), abi=vault_abi)
    
    # Load User Address
    account = web3.eth.account.from_key(private_key)
    user_address = account.address
    st.sidebar.success(f"Connected: {user_address}")

elif private_key and not vault_address:
    st.sidebar.warning("Enter Vault Address!")
elif vault_address and not private_key:
    st.sidebar.warning("Enter Private Key!")

# ----------------------------
# Deposit ETH
# ----------------------------
st.header("📥 Deposit ETH")

deposit_amount = st.number_input("Enter amount to deposit (ETH)", min_value=0.001, step=0.001, format="%.6f")

if st.button("🚀 Deposit"):
    if user_address and vault:
        deposit_txn = vault.functions.deposit().build_transaction({
            'from': user_address,
            'value': web3.to_wei(deposit_amount, 'ether'),
            'gas': 300000,
            'gasPrice': web3.to_wei('10', 'gwei'),
            'nonce': web3.eth.get_transaction_count(user_address),
        })
        
        signed_txn = web3.eth.account.sign_transaction(deposit_txn, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        st.success(f"Deposit Submitted! TX Hash: {web3.to_hex(tx_hash)}")
    else:
        st.error("Wallet and Vault must be connected!")

# ----------------------------
# Withdraw ETH
# ----------------------------
st.header("📤 Withdraw ETH")

withdraw_amount = st.number_input("Enter amount to withdraw (ETH)", min_value=0.001, step=0.001, format="%.6f")

if st.button("💸 Withdraw"):
    if user_address and vault:
        withdraw_txn = vault.functions.withdraw(web3.to_wei(withdraw_amount, 'ether')).build_transaction({
            'from': user_address,
            'gas': 300000,
            'gasPrice': web3.to_wei('10', 'gwei'),
            'nonce': web3.eth.get_transaction_count(user_address),
        })
        
        signed_txn = web3.eth.account.sign_transaction(withdraw_txn, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        st.success(f"Withdrawal Submitted! TX Hash: {web3.to_hex(tx_hash)}")
    else:
        st.error("Wallet and Vault must be connected!")

# ----------------------------
# User Deposit & Reward Info
# ----------------------------
st.header("📊 Your Vault Info")

if user_address and vault:
    deposit, rewards, auto_compounding = vault.functions.getUserInfo(user_address).call()
    st.metric(label="💰 Deposit (ETH)", value=f"{web3.from_wei(deposit, 'ether'):.6f}")
    st.metric(label="🎁 Rewards (ETH)", value=f"{web3.from_wei(rewards, 'ether'):.6f}")
    st.metric(label="⚙️ Auto-Compounding", value="Enabled" if auto_compounding else "Disabled")

# ----------------------------
# Vault Stats
# ----------------------------
st.header("🏦 Vault Overview")

if vault:
    total_eth = vault.functions.getTotalETH().call()
    st.metric(label="🏛️ Total ETH in Vault", value=f"{web3.from_wei(total_eth, 'ether'):.6f}")

# ----------------------------
# Contributors List
# ----------------------------
st.header("🤝 Contributors")

if vault:
    user_addresses = vault.functions.getAllUsers().call()

    if len(user_addresses) > 0:
        for addr in user_addresses:
            user_deposit, _, _ = vault.functions.getUserInfo(addr).call()
            if user_deposit > 0:
                st.write(f"🔹 {addr}: {web3.from_wei(user_deposit, 'ether')} ETH")
    else:
        st.info("No contributors yet.")

