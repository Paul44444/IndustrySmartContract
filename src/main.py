import sys
import time
from mamba_notary import mock_mamba_evaluate
from blockchain_bridge import send_to_blockchain

def run_industrial_agent(log_data):
    """
    The main loop for an Industrial AI Agent.
    1. Receives data from a factory machine.
    2. Runs Mamba SSM to check for anomalies.
    3. If data is clean, sends a cryptographic proof to the blockchain.
    """
    print("\n--- 🤖 Starting AI Agent Pipeline ---")
    
    # Step 1: Evaluate with Mamba
    is_valid, fingerprint = mock_mamba_evaluate(log_data)
    
    if not is_valid:
        print("🚨 AI Alert: Anomaly detected in data. Action: REJECTED.")
        return False

    print(f"✅ AI Analysis: Data is verified. Fingerprint: {fingerprint}")
    
    # Step 2: Notarize on Blockchain
    print("🌐 Initiating Blockchain Notarization...")
    try:
        # Note: This will only work once you fill in your .env and Contract Address
        tx_hash = send_to_blockchain(fingerprint)
        print(f"🎉 Success! Data secured on-chain.")
        print(f"🔗 View Proof: https://sepolia.basescan.org/tx/{tx_hash}")
        return True
    except Exception as e:
        print(f"⚠️ Blockchain Bridge Error: {e}")
        print("Hint: Did you deploy your contract and update the address in blockchain_bridge.py?")
        return False

if __name__ == "__main__":
    # Simulate a stream of data from a CNC machine
    test_logs = [
        "CNC_01: RPM=3000, TEMP=72C, STATUS=OK",
        "CNC_01: RPM=3500, TEMP=98C, STATUS=ERROR_OVERHEAT", # This one should fail
        "CNC_01: RPM=2900, TEMP=70C, STATUS=OK"
    ]
    
    for log in test_logs:
        print(f"\nProcessing Log: {log}")
        run_industrial_agent(log)
        time.sleep(2) # Wait between logs
