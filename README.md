# 🏗️ Industrial-Mamba: Autonomous Physical Arbitrator

**Bridging High-Fidelity Physics with On-Chain Execution via State Space Models (SSMs)**

[![Hackathon](https://img.shields.io/badge/EasyA-Consensus_Hong_Kong-blue?style=for-the-badge&logo=blockchaindotcom)](https://consensus.easyA.io)
[![Model](https://img.shields.io/badge/AI-Mamba--3-green?style=for-the-badge&logo=nvidia)](https://arxiv.org/abs/2312.00752)
[![Field](https://img.shields.io/badge/Industry-DePIN_/_Manufacturing-orange?style=for-the-badge)](#)

---

## 🌐 Why Web3 + Ethereum?
Industrial data is too massive for the blockchain, but industrial *trust* is too fragile for centralized servers. **Industrial-Mamba** solves this by using Ethereum as the global truth layer for physical assets.

* **Trustless Arbitration:** No human needs to verify if a machine broke. The **Mamba AI Judge** provides a cryptographic proof.
* **On-Chain Settlement:** We use **Ethereum Smart Contracts** to handle high-value escrow and automated insurance payouts.
* **DePIN Ready:** Our architecture allows for decentralized physical infrastructure where machines act as independent economic agents.

---

## 🏗️ The Web3 Stack

| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Execution** | **Ethereum / Arbitrum** | Settlement of maintenance fees and SLA penalties. |
| **Inference** | **Mamba-3 (SSM)** | Processing high-fidelity physics telemetry (Vibration/FFT). |
| **Verification** | **zkML (EzKL / Modulus)** | Proving off-chain AI inference was done correctly to the L1. |
| **Identity** | **ERC-6551** | Giving physical machines their own "Smart Accounts" to pay for repairs. |

---

## 🔄 The Workflow (The "Golden Thread")

1.  **Data Capture:** (A) CNC machine vibrations are streamed to an edge-node and (B) A robot, modeled in IsaacLab collects image data
2.  **Mamba Inference:** A Mamba model analyzes the "State Space" of the machine.
3.  **zk-Proof:** The system generates a SNARK proof that the machine is at 90% failure risk.
4.  **Ethereum Trigger:** The proof is submitted to the `MaintenanceEscrow.sol` contract.
5.  **Settlement:** The contract automatically hires a repair bot/technician and locks the payment.

---

## 📜 Smart Contract Example (Solidity)
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract IndustrialArbitrator {
    address public machineOwner;
    bool public maintenanceRequired;

    // Triggered by the Mamba-zkML Oracle
    function triggerMaintenance(bytes32 proofHash) external {
        // Verification logic for the Mamba-based proof
        maintenanceRequired = true;
        emit MaintenanceTriggered(proofHash);
    }
}
```


## 🌟 The Vision
Current smart contracts are "blind" to the complexity of the physical world. They can handle simple temperature thresholds, but they cannot interpret the **vibration signatures** of a failing CNC bearing or the **harmonic distortion** in a power grid.

**Industrial-Mamba** is a decentralized "Subjective Oracle." It leverages the **Mamba architecture (SSM)** to process high-frequency industrial telemetry and verify Service Level Agreements (SLAs) on-chain.

### Why Mamba?
Traditional Transformers suffer from $O(N^2)$ complexity, making real-time industrial monitoring expensive. Mamba provides **Linear Scaling $O(N)$**, allowing us to:
1.  Process **infinite context windows** of sensor logs.
2.  Run inference at the **edge** (factory floor) with minimal latency.
3.  Maintain a continuous "Physical State" of high-value assets.

---

## 🛠️ System Architecture

graph TD
    subgraph Data_Collection [Multimodal Data Acquisition]
        A1[CNC/Physics Sensors] -->|Time-Series Logs| B
        A2[IsaacLab Robot Sim] -->|PNG Vision Frames| B
    end

    B(Mamba-3 Inference Engine) -->|Anomaly Detection| C{AI Judge}
    
    C -->|Verified| D[zk-Proof Generation]
    C -->|Alert| G[Log Local Error]
    
    D -->|Hash + Proof| E[Smart Contract: Ethereum/Base]
    E -->|Automated Payout| F[Maintenance Crew / Insurance]

    %% Styling for clarity
    style Data_Collection fill:#f9f9f9,stroke:#333,stroke-dasharray: 5 5
    style B fill:#e1f5fe,stroke:#01579b
    style E fill:#e8f5e9,stroke:#2e7d32

## 🏗️ Repository Structure

```text
industrial-mamba/
├── data/               # High-fidelity CNC & Physics datasets (NASA Milling)
├── src/                # Python source code for AI and Physics modeling
│   ├── model.py        # Mamba-3 SSM Architecture implementation
│   └── processor.py    # Signal processing and FFT logic for CNC data
├── contracts/          # Solidity Smart Contracts (Ethereum/Sui)
│   └── Arbitrator.sol  # On-chain maintenance escrow and logic
├── tests/              # Unit tests for both AI models and contracts
├── requirements.txt    # Python dependencies
└── package.json        # Web3 and Hardhat/Thirdweb dependencies
```

## **🚀 Getting Started**
Follow these steps to set up the environment and run the industrial arbiter locally.

1. Clone the repository
```
git clone [https://github.com/your-username/industrial-mamba.git](https://github.com/your-username/industrial-mamba.git)
cd industrial-mamba
```
2. Set Up Python Environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. Install Web3 Tools
```
npm install
npx thirdweb deploy
```
4. Set Up IsaacLab repository:
Set up an NVIDIA IsaacLab repository of the Franka robot ([Overview over IsaacLabEnvs](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html))

5. Adjust paths and File locations:
Add the modified environment from the Github folder src/IsaacLabEnvModified into your IsaacLab directory structure at the "manipulation"-directory. This can have a path e.g.
```
/home/user/miniconda3/envs/env_isaaclab1/lib/python3.11/site-packages/isaaclab/source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/.
```
Moreover, the file train.py should be added at the reinforcement_learning path under the learning strategy, e.g. for skrl it could be:
```
/home/user/IsaacLab/scripts/reinforcement_learning/skrl.
```
