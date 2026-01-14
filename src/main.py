import sys
import time
from mamba_notary import mamba_evaluate_cnc, evaluate_isaac_image
from blockchain_bridge import send_to_blockchain
import pandas as pd
from mamba_ssm import Mamba

def load_industrial_data(file_path=None):
    # Load the high-fidelity CSV
    df = pd.read_csv(file_path)
    
    # Selecting the "Physics" columns
    # e.g., Spindle Vibration and Acoustic Emission
    physics_data = df[['vib_spindle', 'AE_spindle']].values
    
    return physics_data

def eval_ims():
    # --- Execution ---
    
    # Currently reading one file; In the future this can be extended to 
    #       reading image series
    image_file = "../data/images/frame_1766248364.2299833.png"

    valid, hsh = None, None
    if os.path.exists(image_file):
        valid, hsh = evaluate_isaac_image(image_file)
        print(f"🖼 Image: {image_file}")
        print(f"✅ AI Verified: {valid}")
        print(f"🔗 Blockchain Hash: {hsh}")
    
    return valid, hsh 

def run_industrial_agent(log_data):
    """
    The main loop for an Industrial AI Agent.
    1. Receives data from a factory machine.
    2. Runs Mamba SSM to check for anomalies.
    3. If data is clean, sends a cryptographic proof to the blockchain.
    """
    print("\n--- 🤖 Starting AI Agent Pipeline ---")
    
    # Step 1: Evaluate with Mamba
    is_valid_cnc, fingerprint = mamba_evaluate_cnc(log_data)
    is_valid_im, hsh  = mamba_evaluate_cnc(log_data)
    is_valid = is_valid_cnc and is_valid_im

    if not is_valid:
        print("🚨 AI Alert: Anomaly detected in data. Action: REJECTED.")
        return False

    print(f"✅ AI Analysis: Data is verified. Fingerprint: {fingerprint}, hsh: {hsh}")
    
    # Step 2: Notarize on Blockchain
    print("🌐 Initiating Blockchain Notarization...")
    try:
        tx_hash = send_to_blockchain(fingerprint)
        tx_hash_im = send_to_blockchain(hsh)
        print(f"🎉 Success! Data secured on-chain.")
        print(f"🔗 View Proof for CNC: https://sepolia.basescan.org/tx/{tx_hash}")
        print(f"🔗 View Proof for im: https://sepolia.basescan.org/tx/{tx_hash_im}")
        return True
    except Exception as e:
        print(f"⚠️ Blockchain Bridge Error: {e}")
        print("Hint: Did you deploy your contract and update the address in blockchain_bridge.py?")
        return False


if __name__ == "__main__":
    
    # Fetch CNC data
    data = load_industrial_data(file_path="../data/mill.csv")
    
    # Apply mamba agent and submit to blockchain
    run_industrial_agent(data)
    time.sleep(2) # Wait between logs
