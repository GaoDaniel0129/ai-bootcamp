"""db.py：聊天消息的存取"""
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "chat.db"

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT    NOT NULL,
            role       TEXT    NOT NULL,
            content    TEXT,
            created_at TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_session ON messages(session_id)")
    conn.commit()
    conn.close()

def get_history(session_id, limit=30):
    """取某会话最近 limit 条消息（按时间正序返回）"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT role, content FROM ("
        "  SELECT id, role, content FROM messages "
        "  WHERE session_id = ? ORDER BY id DESC LIMIT ?"
        ") ORDER BY id ASC",          # 先取最新 N 条，再倒回正序
        (session_id, limit),
    ).fetchall()
    conn.close()
    return [{"role": r["role"], "content": r["content"]} for r in rows]

def save_message(session_id, role, content):
    conn = get_conn()
    conn.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content),
    )
    conn.commit()
    conn.close()

def clear_session(session_id):
    conn = get_conn()
    conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()