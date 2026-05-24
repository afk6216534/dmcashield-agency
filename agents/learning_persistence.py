import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

LEARNING_DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), "learning_data.db")

def get_conn():
    conn = sqlite3.connect(LEARNING_DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS memory_bank (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS mistakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            context TEXT DEFAULT '{}',
            failure_reason TEXT DEFAULT '',
            timestamp TEXT NOT NULL,
            times_failed INTEGER DEFAULT 1,
            last_attempt TEXT,
            improvement_applied INTEGER DEFAULT 0,
            fixed_at TEXT
        );
        CREATE TABLE IF NOT EXISTS mistake_patterns (
            category TEXT PRIMARY KEY,
            count INTEGER DEFAULT 1,
            reasons TEXT DEFAULT '[]'
        );
        CREATE TABLE IF NOT EXISTS improvement_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            fixed_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS learning_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            outcome TEXT NOT NULL,
            context TEXT DEFAULT '{}',
            timestamp TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS learning_patterns (
            action TEXT PRIMARY KEY,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()

init_db()


class SQLiteMemoryBank:
    def __init__(self, namespace="default"):
        self.namespace = namespace

    def save(self, memory: Dict) -> bool:
        try:
            conn = get_conn()
            now = datetime.utcnow().isoformat()
            conn.execute(
                "INSERT OR REPLACE INTO memory_bank (key, value, updated_at) VALUES (?, ?, ?)",
                (self.namespace, json.dumps(memory), now)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"MemoryBank save error: {e}")
            return False

    def load(self) -> Dict:
        try:
            conn = get_conn()
            row = conn.execute(
                "SELECT value FROM memory_bank WHERE key = ?", (self.namespace,)
            ).fetchone()
            conn.close()
            if row:
                return json.loads(row["value"])
        except Exception as e:
            print(f"MemoryBank load error: {e}")
        return {"mistakes": [], "learnings": [], "patterns": [], "improvements": []}


class SQLiteMistakeTracker:
    def __init__(self):
        pass

    def record_mistake(self, category: str, context: Dict, failure_reason: str) -> Dict:
        conn = get_conn()
        now = datetime.utcnow().isoformat()
        cur = conn.execute(
            "INSERT INTO mistakes (category, context, failure_reason, timestamp, last_attempt) VALUES (?, ?, ?, ?, ?)",
            (category, json.dumps(context), failure_reason, now, now)
        )
        mistake_id = cur.lastrowid

        existing = conn.execute(
            "SELECT count, reasons FROM mistake_patterns WHERE category = ?", (category,)
        ).fetchone()
        if existing:
            reasons = json.loads(existing["reasons"])
            if failure_reason not in reasons:
                reasons.append(failure_reason)
            conn.execute(
                "UPDATE mistake_patterns SET count = count + 1, reasons = ? WHERE category = ?",
                (json.dumps(reasons), category)
            )
        else:
            conn.execute(
                "INSERT INTO mistake_patterns (category, count, reasons) VALUES (?, 1, ?)",
                (category, json.dumps([failure_reason]))
            )

        conn.commit()
        conn.close()

        return {
            "id": mistake_id,
            "category": category,
            "context": context,
            "failure_reason": failure_reason,
            "timestamp": now,
            "improvement_applied": False
        }

    def get_failure_patterns(self) -> List[Dict]:
        conn = get_conn()
        rows = conn.execute(
            "SELECT category, count, reasons FROM mistake_patterns ORDER BY count DESC"
        ).fetchall()
        conn.close()
        return [
            {"category": r["category"], "failures": r["count"], "reasons": json.loads(r["reasons"])}
            for r in rows
        ]

    def mark_improvement(self, category: str) -> Dict:
        conn = get_conn()
        now = datetime.utcnow().isoformat()
        row = conn.execute(
            "SELECT id FROM mistakes WHERE category = ? AND improvement_applied = 0 ORDER BY id DESC LIMIT 1",
            (category,)
        ).fetchone()
        if row:
            conn.execute(
                "UPDATE mistakes SET improvement_applied = 1, fixed_at = ? WHERE id = ?",
                (now, row["id"])
            )
            conn.execute(
                "INSERT INTO improvement_log (category, fixed_at) VALUES (?, ?)",
                (category, now)
            )
            conn.commit()
            conn.close()
            return {"status": "fixed", "category": category, "mistake_id": row["id"]}
        conn.close()
        return {"status": "no_mistake_found"}

    def mark_fixed_by_id(self, mistake_id: int) -> Dict:
        conn = get_conn()
        now = datetime.utcnow().isoformat()
        row = conn.execute(
            "SELECT id, category FROM mistakes WHERE id = ? AND improvement_applied = 0",
            (mistake_id,)
        ).fetchone()
        if row:
            conn.execute(
                "UPDATE mistakes SET improvement_applied = 1, fixed_at = ? WHERE id = ?",
                (now, row["id"])
            )
            conn.execute(
                "INSERT INTO improvement_log (category, fixed_at) VALUES (?, ?)",
                (row["category"], now)
            )
            conn.commit()
            conn.close()
            return {"status": "fixed", "mistake_id": row["id"], "category": row["category"]}
        conn.close()
        return {"status": "not_found"}

    def get_mistake_count(self) -> int:
        conn = get_conn()
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM mistakes WHERE improvement_applied = 0"
        ).fetchone()
        conn.close()
        return row["cnt"] if row else 0


class SQLiteLearningEngine:
    def __init__(self):
        pass

    def learn(self, action: str, outcome: str, context: Dict) -> Dict:
        conn = get_conn()
        now = datetime.utcnow().isoformat()

        conn.execute(
            "INSERT INTO learning_entries (action, outcome, context, timestamp) VALUES (?, ?, ?, ?)",
            (action, outcome, json.dumps(context), now)
        )

        existing = conn.execute(
            "SELECT wins, losses FROM learning_patterns WHERE action = ?", (action,)
        ).fetchone()
        is_success = outcome in ["success", "won", "gained", "profit"]
        if existing:
            if is_success:
                conn.execute("UPDATE learning_patterns SET wins = wins + 1 WHERE action = ?", (action,))
            else:
                conn.execute("UPDATE learning_patterns SET losses = losses + 1 WHERE action = ?", (action,))
        else:
            conn.execute(
                "INSERT INTO learning_patterns (action, wins, losses) VALUES (?, ?, ?)",
                (action, 1 if is_success else 0, 0 if is_success else 1)
            )

        successes = conn.execute(
            "SELECT COUNT(*) as cnt FROM learning_entries WHERE outcome IN ('success','won','gained','profit')"
        ).fetchone()["cnt"]
        failures = conn.execute(
            "SELECT COUNT(*) as cnt FROM learning_entries WHERE outcome NOT IN ('success','won','gained','profit')"
        ).fetchone()["cnt"]
        total = successes + failures

        conn.commit()
        conn.close()

        return {
            "action": action,
            "outcome": outcome,
            "context": context,
            "timestamp": now,
            "total_successes": successes,
            "total_failures": failures,
            "success_rate": successes / max(1, total)
        }

    def get_best_actions(self) -> List[Dict]:
        conn = get_conn()
        rows = conn.execute(
            "SELECT action, wins, losses FROM learning_patterns"
        ).fetchall()
        conn.close()
        best = []
        for r in rows:
            total = r["wins"] + r["losses"]
            if total > 0:
                best.append({
                    "action": r["action"],
                    "win_rate": r["wins"] / total,
                    "total_attempts": total
                })
        return sorted(best, key=lambda x: x["win_rate"], reverse=True)[:5]

    def get_improvement_suggestions(self) -> List[str]:
        conn = get_conn()
        rows = conn.execute(
            "SELECT action, wins, losses FROM learning_patterns"
        ).fetchall()
        conn.close()
        suggestions = []
        for r in rows:
            total = r["wins"] + r["losses"]
            if total > 0:
                win_rate = r["wins"] / total
                if win_rate < 0.4:
                    suggestions.append(
                        f"Improve {r['action']} strategy (current win rate: {int(win_rate * 100)}%)"
                    )
        return suggestions
