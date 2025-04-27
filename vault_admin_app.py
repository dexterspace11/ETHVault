import streamlit as st
import streamlit.components.v1 as components
from web3 import Web3
from eth_account import Account

# -------------------------------
# Configuration
# -------------------------------
st.set_page_config(page_title="ETH Vault Admin Panel", layout="wide")

RPC_URL = "https://mainnet.infura.io/v3/e0fcce634506410b87fc31064eed915a"  # <-- Change this to your Infura/Alchemy RPC
CONTRACT_ADDRESS = "0x4d1748A9997A9E201d65A544d79189dACc9485E2"  # <-- Your Vault contract

# Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# ABI - Insert your ETHVault ABI below
contract_abi = [
    {
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTotalETH",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "userAddr", "type": "address"}],
        "name": "getUserInfo",
        "outputs": [
            {"internalType": "uint256", "name": "depositBalance", "type": "uint256"},
            {"internalType": "uint256", "name": "currentRewards", "type": "uint256"},
            {"internalType": "bool", "name": "autoCompounding", "type": "bool"},
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "admin",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address payable", "name": "target", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "sendExternal",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

# -------------------------------
# Inject JavaScript for Metamask connection
# -------------------------------
st.title("💎 ETH Vault - Admin & User Panel")

connect_html = """
<script>
async function connect() {
    if (window.ethereum) {
        try {
            const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
            const account = accounts[0];
            const display = document.getElementById('account_display');
            display.innerText = account;
            window.parent.postMessage({funcName: 'setAccount', address: account}, "*");
        } catch (error) {
            console.error(error);
        }
    } else {
        alert('Please install Metamask!');
    }
}
</script>

<button onclick="connect()">🦊 Connect Metamask</button>
<p id="account_display" style="color:green; font-weight:bold; font-size:20px;"></p>
"""

components.html(connect_html, height=200)

# Wallet connection simulation (manual input until full two-way comms is done)
account = st.text_input("Paste your connected Metamask Wallet Address", key="wallet_address")

# -------------------------------
# Main Interface
# -------------------------------
if account:
    st.success(f"Connected Wallet: {account}")

    admin_address = contract.functions.admin().call()
    is_admin = (account.lower() == admin_address.lower())

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["Deposit", "Withdraw", "View My Info", "Admin Panel"])

    if page == "Deposit":
        st.subheader("📥 Deposit ETH")
        eth_amount = st.number_input("Amount to Deposit (ETH)", min_value=0.001, step=0.001, format="%.5f")
        if st.button("Deposit"):
            st.warning("⚡ Please deposit manually to the contract address using Metamask.")
            st.info(f"Contract Address: {CONTRACT_ADDRESS}")

    elif page == "Withdraw":
        st.subheader("📤 Withdraw from Vault")
        withdraw_amount = st.number_input("Amount to Withdraw (ETH)", min_value=0.001, step=0.001, format="%.5f")
        if st.button("Request Withdraw"):
            st.warning("⚡ Withdrawal will require Metamask interaction - to be enabled soon.")
            st.info("Please use Remix or Frontend integration to withdraw.")

    elif page == "View My Info":
        st.subheader("🧾 My Vault Info")
        try:
            depositBalance, currentRewards, autoCompounding = contract.functions.getUserInfo(account).call()
            st.metric("Deposit Balance (ETH)", web3.from_wei(depositBalance, 'ether'))
            st.metric("Current Rewards (ETH)", web3.from_wei(currentRewards, 'ether'))
            st.metric("Auto-Compounding", "Enabled" if autoCompounding else "Disabled")
        except Exception as e:
            st.error("Error fetching user info. Make sure your address has interacted with the contract.")

        st.divider()
        total_eth = contract.functions.getTotalETH().call()
        st.metric("Total ETH in Vault", web3.from_wei(total_eth, 'ether'))

    elif page == "Admin Panel":
        if not is_admin:
            st.error("Only Admin can access this page.")
        else:
            st.subheader("🔐 Admin Controls")
            target_address = st.text_input("Target Address to Send ETH")
            send_amount = st.number_input("Amount to Send (ETH)", min_value=0.001, step=0.001, format="%.5f")
            if st.button("Send ETH"):
                st.warning("⚡ Admin send will require Metamask interaction - to be enabled soon.")
                st.info("Use Remix for now for admin 'sendExternal' function.")
else:
    st.warning("🦊 Connect your wallet first to use the dApp.")

