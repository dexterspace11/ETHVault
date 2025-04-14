import streamlit as st
from web3 import Web3
import json
from contract_instance import contract, web3

st.set_page_config(page_title="ETH Vault", layout="centered")
st.title("🔐 ETH Vault DApp")

# User Wallet Input
user_address = st.text_input("Enter your wallet address:")

# Load user data if address is provided
if user_address:
    try:
        user_info = contract.functions.getUserInfo(user_address).call()
        deposit_balance = web3.from_wei(user_info[0], "ether")
        rewards = web3.from_wei(user_info[1], "ether")
        auto_compounding = user_info[2]

        st.success(f"💰 Deposit: {deposit_balance} ETH")
        st.success(f"🎁 Rewards: {rewards} ETH")
        st.info(f"Auto-Compounding: {'Enabled' if auto_compounding else 'Disabled'}")

    except Exception as e:
        st.error("Couldn't fetch user data. Make sure the address is valid.")
        st.stop()

# Deposit (Info Only)
st.markdown("---")
st.subheader("Deposit ETH to Vault")

st.markdown(
    """
    1. Open your MetaMask wallet  
    2. Send ETH to this vault address:
    """
)
st.code(contract.address)
st.warning("Make sure you're on the same network!")

# Withdraw info
st.markdown("---")
st.subheader("Withdraw ETH + Rewards")
st.markdown("Currently, withdrawals can only be executed via Remix or backend interaction.")
