import torch
from mamba_ssm import Mamba
import hashlib

import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from mamba_ssm import Mamba
import hashlib
import os

# Configuration for a small "Edge-sized" Mamba model
# d_model: the number of features (e.g., Temp, RPM, Vibration)
# d_state: the "memory" of the SSM
model = Mamba(
    d_model=16, 
    d_state=16, 
    d_conv=4, 
    expand=2
).to("cuda") # Use "cpu" if you don't have an NVIDIA GPU

# 2. Define a Simple Vision Mamba Evaluator
class VisionMambaEvaluator(nn.Module):
    def __init__(self):
        super().__init__()
        # d_model=768 is common for vision features
        self.mamba = Mamba(d_model=768, d_state=16, d_conv=4, expand=2)
        self.patch_embed = nn.Linear(3 * 16 * 16, 768) # 16x16 pixel patches

    def forward(self, x):
        # x shape: [1, 3, 128, 128] -> Divide into patches
        # This is a simplified patchification logic
        patches = x.unfold(2, 16, 16).unfold(3, 16, 16)
        patches = patches.contiguous().view(1, 768, -1).transpose(1, 2) 
        
        # Pass through Mamba
        features = self.mamba(patches)
        return torch.mean(features) # Return a combined "Integrity Score"

def mamba_evaluate_cnc(sensor_values):
    """
    Actual Mamba SSM Inference.
    sensor_values: List of floats [temp, rpm, vibration, ...]
    """
    # Convert input to a Torch Tensor (Batch, Length, Dim)
    # We treat the current reading as a sequence of length 1
    input_data = torch.tensor(sensor_values).float().unsqueeze(0).unsqueeze(0)
    
    with torch.no_grad():
        # Mamba processes the sequence and updates its internal state
        output = model(input_data)
        
        # In a real Anomaly Detection scenario:
        # We would compare 'output' to 'input_data'. 
        # Large difference (reconstruction error) = Anomaly.
        reconstruction_error = torch.abs(input_data - output).mean().item()
        
    # Threshold for CNC Anomaly (0.5 is an example)
    is_valid = reconstruction_error < 0.5
    
    # Create the cryptographic hash of the data for the blockchain
    data_str = ",".join(map(str, sensor_values))
    fingerprint = hashlib.sha256(data_str.encode()).hexdigest()
    
    return is_valid, fingerprint, reconstruction_error

def evaluate_isaac_image(image_path):

    # 1. Image Preprocessing for Mamba
    # We resize to 128x128 and flatten patches into a sequence
    preprocess = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    if not os.path.exists(image_path):
        return False, "File not found"

    # Load the images taken by the camera attached to the robot in IsaacLab
    img = Image.open(image_path).convert('RGB')
    img_tensor = preprocess(img).unsqueeze(0)

    # AI Inference
    model = VisionMambaEvaluator()
    with torch.no_grad():
        score = model(img_tensor).item()

    # Create Hash of the raw image bytes for the Blockchain
    with open(image_path, "rb") as f:
        img_hash = hashlib.sha256(f.read()).hexdigest()

    # Logic: If the 'vision score' is within a normal range (example threshold)
    is_valid = -1.0 < score < 1.0 
    return is_valid, img_hash

if __name__ == "__main__":
    # For testing: 
    # [Temp, RPM, Vibration, ...]
    normal_data = [70.5, 3000.0, 0.02, 1.2, 0.5, 70.0, 30.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    valid, hsh, err = mamba_evaluate_cnc(normal_data)
    print(f"Mamba Result: {'✅ Valid' if valid else '🚨 Anomaly'} | Error Score: {err:.4f}")