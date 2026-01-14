import os
from web3 import Web3
from dotenv import load_dotenv

# 1. Load your credentials (we will put these in a .env file for safety)
load_dotenv()

# --- CONFIGURATION (Fill these after deployment) ---
# This is the RPC URL for Base Sepolia (standard for 2026)
RPC_URL = "https://base-sepolia.g.alchemy.com/v2/ALC_smartcontractindustry_9kL2m8n4p1q" # To the Github user: replace this by your respective url  
CONTRACT_ADDRESS = "0xCAFEbabe45678901234567890123456789012345" # To the Github user: Replace this with your respective contract address
PRIVATE_KEY = os.getenv("PRIVATE_KEY") # private key
SENDER_ADDRESS = "0xDEA0babe12345678901234567890123456789012" # To the Github user: Replace this with your respective sender address

# 2. Connect to the Blockchain
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():
    print(f"✅ Connected to Base Sepolia")
else:
    print("❌ Connection Failed")

# 3. Contract ABI (This tells Python what functions exist)
# After deployment, Thirdweb gives you this JSON. Here is the minimal version:
ABI = [
    {
        "inputs": [{"internalType": "string", "name": "_dataHash", "type": "string"}],
        "name": "notarizeData",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def send_to_blockchain(data_hash):
    """
    Sends the AI-generated fingerprint to the smart contract.
    """
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
    
    # Get the 'nonce' (transaction count for your wallet)
    nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)
    
    # Build the transaction
    tx = contract.functions.notarizeData(data_hash).build_transaction({
        'chainId': 84532, # Base Sepolia Chain ID
        'gas': 200000,
        'gasPrice': w3.to_wei('1', 'gwei'),
        'nonce': nonce,
    })
    
    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    
    # Send it!
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"🚀 Transaction sent! Hash: {w3.to_hex(tx_hash)}")
    
    # Wait for confirmation
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"⚓ Confirmed in block: {receipt.blockNumber}")
    return w3.to_hex(tx_hash)

if __name__ == "__main__":
    # Test with a dummy hash
    test_hash = "ipfs://sample_industrial_data_hash"
    # send_to_blockchain(test_hash) 
