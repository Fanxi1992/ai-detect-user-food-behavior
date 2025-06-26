import aiosqlite
from datetime import datetime
from typing import List, Optional
import uuid

class Message:
    def __init__(self, id: str, session_id: str, content: str, is_user: bool, timestamp: datetime):
        self.id = id
        self.session_id = session_id
        self.content = content
        self.is_user = is_user
        self.timestamp = timestamp

class Database:
    def __init__(self, db_path: str = "chatbot.db"):
        self.db_path = db_path
    
    async def init_db(self):
        """初始化数据库表"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    is_user BOOLEAN NOT NULL,
                    timestamp DATETIME NOT NULL
                )
            """)
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_id ON messages(session_id)
            """)
            await db.commit()
    
    async def save_message(self, session_id: str, content: str, is_user: bool) -> Message:
        """保存消息到数据库"""
        message_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO messages (id, session_id, content, is_user, timestamp) VALUES (?, ?, ?, ?, ?)",
                (message_id, session_id, content, is_user, timestamp)
            )
            await db.commit()
        
        return Message(message_id, session_id, content, is_user, timestamp)
    
    async def get_messages(self, session_id: str, limit: int = 100) -> List[Message]:
        """获取会话的消息列表"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, session_id, content, is_user, timestamp FROM messages WHERE session_id = ? ORDER BY timestamp ASC LIMIT ?",
                (session_id, limit)
            )
            rows = await cursor.fetchall()
            
            messages = []
            for row in rows:
                messages.append(Message(
                    id=row[0],
                    session_id=row[1],
                    content=row[2],
                    is_user=bool(row[3]),
                    timestamp=datetime.fromisoformat(row[4])
                ))
            
            return messages
    
    async def clear_messages(self, session_id: str):
        """清空会话的所有消息"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            await db.commit()
    
    async def get_all_sessions(self) -> List[str]:
        """获取所有会话ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT DISTINCT session_id FROM messages")
            rows = await cursor.fetchall()
            return [row[0] for row in rows]