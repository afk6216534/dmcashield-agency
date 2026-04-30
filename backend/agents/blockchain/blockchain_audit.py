"""
Blockchain Audit Trail Integration
=================================
Provides immutable audit trails for critical system actions
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class Block:
    """A single block in the audit chain"""
    def __init__(self, index: int, timestamp: str, data: Dict, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.nonce = 0

    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of block"""
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.data, sort_keys=True)}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int = 2):
        """Simple proof-of-work simulation"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self) -> Dict:
        """Convert block to dictionary"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce
        }

class BlockchainAudit:
    """Immutable audit trail using blockchain principles"""

    def __init__(self, chain_file: str = "F:/Anti gravity projects/Dmca company/dmcashield-agency/backend/memory/audit_chain.json"):
        self.chain_file = chain_file
        self.chain = []
        self.difficulty = 2
        self.load_chain()
        if not self.chain:
            self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, datetime.utcnow().isoformat(), {
            "action": "genesis",
            "actor": "system",
            "target": "blockchain_audit",
            "status": "initialized"
        }, "0" * 64)
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        self.save_chain()

    def load_chain(self):
        """Load blockchain from file"""
        try:
            with open(self.chain_file, 'r') as f:
                chain_data = json.load(f)
                for block_data in chain_data:
                    block = Block(
                        block_data["index"],
                        block_data["timestamp"],
                        block_data["data"],
                        block_data["previous_hash"]
                    )
                    block.hash = block_data["hash"]
                    block.nonce = block_data["nonce"]
                    self.chain.append(block)
        except FileNotFoundError:
            self.chain = []

    def save_chain(self):
        """Save blockchain to file"""
        chain_data = [block.to_dict() for block in self.chain]
        with open(self.chain_file, 'w') as f:
            json.dump(chain_data, f, indent=2)

    def add_record(self, actor: str, action: str, target: str, status: str, details: Dict = None) -> Block:
        """Add a new record to the audit chain"""
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.utcnow().isoformat(),
            data={
                "actor": actor,
                "action": action,
                "target": target,
                "status": status,
                "details": details or {},
                "event_id": hashlib.sha256(f"{actor}{action}{target}{time.time()}".encode()).hexdigest()[:16]
            },
            previous_hash=previous_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_chain()

        # Also log to persistent memory
        try:
            from agents.memory.persistent_memory import persistent_memory
            persistent_memory.log_audit_event(actor, action, target, status, details)
        except ImportError:
            pass

        return new_block

    def verify_chain(self) -> bool:
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            # Check if current block's hash is valid
            if current.hash != current.calculate_hash():
                return False

            # Check if current block points to previous block
            if current.previous_hash != previous.hash:
                return False

            # Check proof-of-work
            if current.hash[:self.difficulty] != "0" * self.difficulty:
                return False

        return True

    def get_records(self, actor: str = None, action: str = None, limit: int = 100) -> List[Dict]:
        """Retrieve audit records with optional filtering"""
        records = []
        for block in reversed(self.chain):
            data = block.data.copy()
            data["block_index"] = block.index
            data["timestamp"] = block.timestamp
            data["hash"] = block.hash

            if actor and data.get("actor") != actor:
                continue
            if action and data.get("action") != action:
                continue

            records.append(data)
            if len(records) >= limit:
                break

        return records

    def get_statistics(self) -> Dict:
        """Get blockchain statistics"""
        return {
            "total_blocks": len(self.chain),
            "chain_valid": self.verify_chain(),
            "latest_block_hash": self.chain[-1].hash if self.chain else None,
            "difficulty": self.difficulty,
            "chain_file": self.chain_file
        }

# Global instance
blockchain_audit = BlockchainAudit()