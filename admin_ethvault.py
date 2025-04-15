import streamlit as st
from web3 import Web3
import json
import os
from contract_instance import contract, web3

st.set_page_config(page_title="Vault Admin Panel", layout="centered")
st.title("🔐 ETH Vault - Admin Dashboard")

# Show total ETH in contract
st.subheader("📊 Vault Overview")
try:
    total_eth = contract.functions.getTotalETH().call()
    total_eth_ether = web3.from_wei(total_eth, "ether")
    st.success(f"💼 Total ETH in Vault: {total_eth_ether} ETH")
except Exception as e:
    st.error(f"Error fetching total ETH: {str(e)}")

# View Contributor Info
st.markdown("---")
st.subheader("👥 Check Contributor Info")

contrib_address = st.text_input("Enter contributor address:")

if contrib_address:
    try:
        user_info = contract.functions.getUserInfo(contrib_address).call()
        deposit = web3.from_wei(user_info[0], "ether")
        rewards = web3.from_wei(user_info[1], "ether")
        auto_comp = user_info[2]

        st.success(f"Deposit: {deposit} ETH")
        st.success(f"Rewards: {rewards} ETH")
        st.info(f"Auto-Compounding: {'Enabled' if auto_comp else 'Disabled'}")
    except Exception as e:
        st.error("Couldn't fetch contributor data. Check the address.")

# Withdraw Notice
st.markdown("---")
st.subheader("⚠️ Withdraw ETH + Rewards")
st.warning("Withdrawals should be executed via Remix or backend scripts with admin privileges.")
