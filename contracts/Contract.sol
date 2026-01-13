// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataNotary {
    // We store a 'fingerprint' (hash) of the data and the timestamp
    struct Record {
        string dataHash; // The IPFS link or file hash
        uint256 timestamp;
        address uploader;
    }

    mapping(string => Record) public records;

    // This function saves the data fingerprint to the blockchain
    function notarizeData(string memory _dataHash) public {
        require(records[_dataHash].timestamp == 0, "Data already notarized!");
        
        records[_dataHash] = Record({
            dataHash: _dataHash,
            timestamp: block.timestamp,
            uploader: msg.sender
        });
    }
}
