import streamlit as st
from web3 import Web3
from streamlit_etherconnect import ether_connect

# -------------------------------
# Configuration
# -------------------------------
st.set_page_config(page_title="ETH Vault Admin Panel", layout="wide")

# RPC URL (Example for local Ganache or Sepolia Testnet RPC)
RPC_URL = "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # 🔥 CHANGE THIS
CONTRACT_ADDRESS = "0x4d1748A9997A9E201d65A544d79189dACc9485E2"  # 🔥 YOUR Vault Address

# Load Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# ABI
contract_abi = [  
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "admin",
        "outputs": [
            {"internalType": "address", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "autoCompoundAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "userAddr", "type": "address"}],
        "name": "getUserInfo",
        "outputs": [
            {"internalType": "uint256", "name": "depositBalance", "type": "uint256"},
            {"internalType": "uint256", "name": "currentRewards", "type": "uint256"},
            {"internalType": "bool", "name": "autoCompounding", "type": "bool"}
        ],
        "stateMutability": "view",
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
        "inputs": [],
        "name": "getDonationPool",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "enableAutoCompounding",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "disableAutoCompounding",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "userAddress", "type": "address"}],
        "name": "calculateRewards",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
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
    },
    {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }
]

# Contract instance
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

# -------------------------------
# Streamlit App
# -------------------------------

st.title("💎 ETH Vault - Admin & User Panel")

# Metamask connect
address = ether_connect()

if address:
    st.success(f"Connected: {address}")

    admin_address = contract.functions.admin().call()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Deposit", "Withdraw", "View Info", "Admin Panel"])

    st.sidebar.markdown(f"**Vault Address:** `{CONTRACT_ADDRESS}`")

    # Deposit
    if page == "Deposit":
        st.header("📥 Deposit ETH")

        deposit_amount = st.number_input("Enter deposit amount (ETH)", min_value=0.0001, step=0.0001)

        if st.button("Deposit"):
            tx = {
                'from': address,
                'to': CONTRACT_ADDRESS,
                'value': web3.to_wei(deposit_amount, 'ether'),
                'gas': 200000
            }
            st.info(f"Send {deposit_amount} ETH to Vault address manually using your wallet.")

    # Withdraw
    if page == "Withdraw":
        st.header("📤 Withdraw ETH")

        withdraw_amount = st.number_input("Enter amount to withdraw (ETH)", min_value=0.0001, step=0.0001)

        if st.button("Withdraw"):
            try:
                nonce = web3.eth.get_transaction_count(address)
                tx = contract.functions.withdraw(web3.to_wei(withdraw_amount, 'ether')).build_transaction({
                    'from': address,
                    'nonce': nonce,
                    'gas': 300000
                })
                st.info("Sign this withdraw transaction in your Metamask wallet manually.")
            except Exception as e:
                st.error(f"Error: {e}")

    # View Info
    if page == "View Info":
        st.header("🔎 View My Info")

        user_info = contract.functions.getUserInfo(address).call()

        st.subheader("My Vault Status")
        st.metric("Deposited ETH", f"{web3.from_wei(user_info[0], 'ether')} ETH")
        st.metric("Accrued Rewards", f"{web3.from_wei(user_info[1], 'ether')} ETH")
        st.metric("Auto-Compounding Enabled", user_info[2])

        if user_info[2]:
            if st.button("Disable Auto-Compounding"):
                nonce = web3.eth.get_transaction_count(address)
                tx = contract.functions.disableAutoCompounding().build_transaction({
                    'from': address,
                    'nonce': nonce,
                    'gas': 200000
                })
                st.info("Sign the disable auto-compounding transaction manually.")
        else:
            if st.button("Enable Auto-Compounding"):
                nonce = web3.eth.get_transaction_count(address)
                tx = contract.functions.enableAutoCompounding().build_transaction({
                    'from': address,
                    'nonce': nonce,
                    'gas': 200000
                })
                st.info("Sign the enable auto-compounding transaction manually.")

        st.divider()

        st.subheader("📊 Vault Overview")
        total_eth = contract.functions.getTotalETH().call()
        donation_pool = contract.functions.getDonationPool().call()

        st.metric("Total ETH in Vault", f"{web3.from_wei(total_eth, 'ether')} ETH")
        st.metric("Donation Pool", f"{web3.from_wei(donation_pool, 'ether')} ETH")

    # Admin Panel
    if page == "Admin Panel":
        st.header("🛠 Admin Controls")

        if address.lower() == admin_address.lower():
            target = st.text_input("Target address to send ETH")
            send_amount = st.number_input("Amount to send externally (ETH)", min_value=0.0001, step=0.0001)

            if st.button("Send External Transfer"):
                try:
                    nonce = web3.eth.get_transaction_count(address)
                    tx = contract.functions.sendExternal(Web3.to_checksum_address(target), web3.to_wei(send_amount, 'ether')).build_transaction({
                        'from': address,
                        'nonce': nonce,
                        'gas': 300000
                    })
                    st.info("Sign this external transfer transaction manually in Metamask.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("You are NOT the admin.")
else:
    st.warning("Please connect your Metamask Wallet.")

