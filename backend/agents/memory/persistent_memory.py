"""
XII System Memory - Persistent State Management
=============================================
Handles complete system persistence across restarts with encryption and versioning
"""

import json
import os
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import sqlite3
from cryptography.fernet import Fernet

class XII_PersistentMemory:
    """Persistent memory system with encryption, indexing, and versioning"""

    def __init__(self):
        self.base_path = "F:/Anti gravity projects/Dmca company/dmcashield-agency"
        self.memory_path = f"{self.base_path}/backend/memory"
        self.db_path = f"{self.memory_path}/system_memory.db"
        self.encrypted_path = f"{self.memory_path}/encrypted_storage"
        self.version_path = f"{self.memory_path}/version_history"
        self.repo_index_path = f"{self.memory_path}/repo_index.json"

        # Ensure directories exist
        os.makedirs(self.memory_path, exist_ok=True)
        os.makedirs(self.encrypted_path, exist_ok=True)
        os.makedirs(self.version_path, exist_ok=True)

        # Initialize database
        self.init_database()

        # Generate encryption key if not exists
        if not os.path.exists(f"{self.memory_path}/secret.key"):
            self.generate_encryption_key()

        self.cipher_suite = Fernet(self.load_encryption_key())

        # Load repo index
        self.repo_index = self.load_repo_index()

    def generate_encryption_key(self, key_id: str = None):
        """Generate and save encryption key with rotation support"""
        key = Fernet.generate_key()
        key_id = key_id or datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        key_file = f"{self.memory_path}/secret_{key_id}.key"
        with open(key_file, "wb") as f:
            f.write(key)

        # Update current key reference
        with open(f"{self.memory_path}/secret.key", "wb") as f:
            f.write(key)

        # Save key metadata
        self._save_key_metadata(key_id, key_file)
        return key_id

    def _save_key_metadata(self, key_id: str, key_file: str):
        """Save encryption key metadata for rotation"""
        metadata_file = f"{self.memory_path}/key_metadata.json"
        metadata = {}
        if os.path.exists(metadata_file):
            with open(metadata_file, "r") as f:
                metadata = json.load(f)

        metadata[key_id] = {
            "file": key_file,
            "created": datetime.utcnow().isoformat(),
            "active": True
        }
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

    def load_encryption_key(self):
        """Load encryption key"""
        with open(f"{self.memory_path}/secret.key", "rb") as f:
            return f.read()

    def init_database(self):
        """Initialize SQLite database for persistent storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_state (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                version TEXT,
                data TEXT,
                checksum TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_progress (
                task_id TEXT PRIMARY KEY,
                status TEXT,
                progress_data TEXT,
                last_updated TEXT,
                dependencies TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS department_states (
                department_id TEXT PRIMARY KEY,
                status TEXT,
                data TEXT,
                last_active TEXT,
                connections TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                role TEXT,
                content TEXT,
                metadata TEXT,
                encrypted BOOLEAN DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS repo_index (
                repo_id TEXT PRIMARY KEY,
                name TEXT,
                path TEXT,
                last_sync TEXT,
                status TEXT,
                version TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def encrypt_data(self, data: str) -> str:
        """Encrypt data for secure storage"""
        encrypted = self.cipher_suite.encrypt(data.encode())
        return encrypted.decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt data from secure storage"""
        decrypted = self.cipher_suite.decrypt(encrypted_data.encode())
        return decrypted.decode()

    def save_system_state(self, state: Dict[str, Any], version: str = "1.0") -> str:
        """Save complete system state with versioning"""
        state_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        # Calculate checksum
        state_str = json.dumps(state, sort_keys=True)
        checksum = hashlib.sha256(state_str.encode()).hexdigest()

        # Encrypt sensitive data
        encrypted_data = self.encrypt_data(state_str)

        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO system_state (id, timestamp, version, data, checksum)
            VALUES (?, ?, ?, ?, ?)
        ''', (state_id, timestamp, version, encrypted_data, checksum))

        # Also save to file for quick access
        with open(f"{self.memory_path}/current_state.json", "w") as f:
            f.write(json.dumps(state, indent=2))

        conn.commit()
        conn.close()

        # Create version backup
        self.create_version_backup(state, version)

        return state_id

    def load_system_state(self, state_id: Optional[str] = None) -> Dict[str, Any]:
        """Load most recent system state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if state_id:
            cursor.execute('SELECT * FROM system_state WHERE id = ?', (state_id,))
        else:
            cursor.execute('SELECT * FROM system_state ORDER BY timestamp DESC LIMIT 1')

        result = cursor.fetchone()
        conn.close()

        if result:
            _, _, _, encrypted_data, _ = result
            decrypted = self.decrypt_data(encrypted_data)
            return json.loads(decrypted)

        return {}

    def save_task_progress(self, task_id: str, status: str, progress_data: Dict, dependencies: List = None):
        """Save task progress for resumption"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO task_progress
            (task_id, status, progress_data, last_updated, dependencies)
            VALUES (?, ?, ?, ?, ?)
        ''', (task_id, status, json.dumps(progress_data), datetime.utcnow().isoformat(), json.dumps(dependencies or [])))

        conn.commit()
        conn.close()

    def load_task_progress(self, task_id: str = None) -> Dict:
        """Load task progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if task_id:
            cursor.execute('SELECT * FROM task_progress WHERE task_id = ?', (task_id,))
        else:
            cursor.execute('SELECT * FROM task_progress')

        results = cursor.fetchall()
        conn.close()

        if task_id and results:
            result = results[0]
            return {
                'task_id': result[0],
                'status': result[1],
                'progress_data': json.loads(result[2]),
                'last_updated': result[3],
                'dependencies': json.loads(result[4])
            }
        elif not task_id:
            return {r[0]: {
                'status': r[1],
                'progress_data': json.loads(r[2]),
                'last_updated': r[3],
                'dependencies': json.loads(r[4])
            } for r in results}

        return {}

    def save_department_state(self, department_id: str, status: str, data: Dict, connections: List = None):
        """Save department state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO department_states
            (department_id, status, data, last_active, connections)
            VALUES (?, ?, ?, ?, ?)
        ''', (department_id, status, json.dumps(data), datetime.utcnow().isoformat(), json.dumps(connections or [])))

        conn.commit()
        conn.close()

    def load_department_states(self) -> Dict:
        """Load all department states"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM department_states')
        results = cursor.fetchall()
        conn.close()

        return {r[0]: {
            'status': r[1],
            'data': json.loads(r[2]),
            'last_active': r[3],
            'connections': json.loads(r[4])
        } for r in results}

    def save_conversation(self, role: str, content: str, metadata: Dict = None, encrypted: bool = False):
        """Save conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        message_id = str(uuid.uuid4())
        content_to_save = self.encrypt_data(content) if encrypted else content

        cursor.execute('''
            INSERT INTO conversation_history (id, timestamp, role, content, metadata, encrypted)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (message_id, datetime.utcnow().isoformat(), role, content_to_save, json.dumps(metadata or {}), encrypted))

        conn.commit()
        conn.close()

        return message_id

    def get_conversation_history(self, limit: int = 100) -> List[Dict]:
        """Get conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, timestamp, role, content, metadata, encrypted
            FROM conversation_history
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))

        results = cursor.fetchall()
        conn.close()

        history = []
        for result in results:
            message_id, timestamp, role, content, metadata, encrypted = result
            if encrypted:
                content = self.decrypt_data(content)
            history.append({
                'id': message_id,
                'timestamp': timestamp,
                'role': role,
                'content': content,
                'metadata': json.loads(metadata),
                'encrypted': bool(encrypted)
            })

        return history

    def create_version_backup(self, state: Dict, version: str):
        """Create versioned backup"""
        backup_file = f"{self.version_path}/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{version}.json"

        with open(backup_file, "w") as f:
            f.write(json.dumps(state, indent=2))

        # Keep only last 10 backups
        backups = sorted([f for f in os.listdir(self.version_path) if f.startswith("backup_")])
        if len(backups) > 10:
            for old_backup in backups[:-10]:
                os.remove(f"{self.version_path}/{old_backup}")

    def save_repo_index(self):
        """Save repository index"""
        with open(self.repo_index_path, "w") as f:
            f.write(json.dumps(self.repo_index, indent=2))

    def load_repo_index(self) -> Dict:
        """Load repository index"""
        if os.path.exists(self.repo_index_path):
            with open(self.repo_index_path, "r") as f:
                return json.load(f)
        return {}

    def index_repository(self, name: str, path: str, status: str = "active"):
        """Index a repository for tracking"""
        repo_id = str(uuid.uuid4())
        self.repo_index[repo_id] = {
            "name": name,
            "path": path,
            "last_sync": datetime.utcnow().isoformat(),
            "status": status,
            "version": "1.0"
        }
        self.save_repo_index()

        # Also save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO repo_index
            (repo_id, name, path, last_sync, status, version)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (repo_id, name, path, datetime.utcnow().isoformat(), status, "1.0"))
        conn.commit()
        conn.close()

        return repo_id

    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM system_state')
        system_state_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM task_progress')
        task_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM department_states')
        dept_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM conversation_history')
        conv_count = cursor.fetchone()[0]

        cursor.execute('SELECT MAX(timestamp) FROM system_state')
        last_save = cursor.fetchone()[0]

        conn.close()

        return {
            'system_states': system_state_count,
            'tasks_saved': task_count,
            'departments_saved': dept_count,
            'conversations_saved': conv_count,
            'last_save': last_save,
            'repos_indexed': len(self.repo_index)
        }

    def save_current_session(self, department_status: Dict = None, task_status: Dict = None):
        """Save complete current session state"""
        state = {
            "timestamp": datetime.utcnow().isoformat(),
            "departments": department_status or {},
            "tasks": task_status or {},
            "conversation_history": self.get_conversation_history(50),
            "repo_index": self.repo_index
        }
        return self.save_system_state(state, "session_auto")

    def restore_session(self) -> Dict:
        """Restore last session state"""
        return self.load_system_state()

    def log_audit_event(self, actor: str, action: str, target: str, status: str, details: Dict = None):
        """Log an audit event for security tracking"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "actor": actor,
            "action": action,
            "target": target,
            "status": status,
            "details": details or {},
            "fingerprint": hashlib.sha256(f"{actor}{action}{target}{status}".encode()).hexdigest()[:16]
        }

        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT,
                created TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO audit_log (event, created)
            VALUES (?, ?)
        ''', (json.dumps(event), datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()

        # Also save to encrypted conversation history
        self.save_conversation(
            role="audit",
            content=json.dumps(event),
            encrypted=True,
            metadata={"actor": actor, "action": action}
        )

        return event

    def get_audit_log(self, limit=100, actor=None, action=None) -> List[Dict]:
        """Retrieve audit log entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = 'SELECT event, created FROM audit_log ORDER BY created DESC LIMIT ?'
        params = [limit]

        if actor:
            query = query.replace('ORDER BY', 'WHERE event LIKE ? ORDER BY')
            params.insert(0, f'%"actor":"{actor}"%')

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        return [json.loads(r[0]) for r in results]

# Global persistent memory instance
persistent_memory = XII_PersistentMemory()
