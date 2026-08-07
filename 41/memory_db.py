import sqlite3
from typing import List, Dict, Any


class MemoryDB:
    def __init__(self, db_path: str = "history.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def add_message(self, user_id: int, role: str, content: str) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content)
        )
        conn.commit()
        conn.close()

    def get_last_messages(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content FROM history WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        
        # Reverse to get chronological order
        messages = [{"role": row["role"], "content": row["content"]} for row in rows]
        return messages[::-1]

    def clear_history(self, user_id: int) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM history WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
