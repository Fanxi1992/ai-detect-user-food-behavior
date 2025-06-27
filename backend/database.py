import aiosqlite
from datetime import datetime
from typing import List, Optional
import uuid
import json

class Message:
    def __init__(self, id: str, session_id: str, content: str, is_user: bool, timestamp: datetime, health_behavior_data: Optional[str] = None):
        self.id = id
        self.session_id = session_id
        self.content = content
        self.is_user = is_user
        self.timestamp = timestamp
        self.health_behavior_data = health_behavior_data

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
                    timestamp DATETIME NOT NULL,
                    health_behavior_data TEXT
                )
            """)
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_id ON messages(session_id)
            """)
            
            # 为现有表添加新字段（如果不存在）
            try:
                await db.execute("ALTER TABLE messages ADD COLUMN health_behavior_data TEXT")
            except Exception:
                # 字段已存在，忽略错误
                pass
            
            await db.commit()
    
    async def save_message(self, session_id: str, content: str, is_user: bool, health_behavior_data: Optional[dict] = None) -> Message:
        """保存消息到数据库"""
        message_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        # 将健康行为数据转换为JSON字符串
        health_behavior_json = None
        if health_behavior_data:
            health_behavior_json = json.dumps(health_behavior_data)
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO messages (id, session_id, content, is_user, timestamp, health_behavior_data) VALUES (?, ?, ?, ?, ?, ?)",
                (message_id, session_id, content, is_user, timestamp, health_behavior_json)
            )
            await db.commit()
        
        return Message(message_id, session_id, content, is_user, timestamp, health_behavior_json)
    
    async def get_messages(self, session_id: str, limit: int = 100) -> List[Message]:
        """获取会话的消息列表"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, session_id, content, is_user, timestamp, health_behavior_data FROM messages WHERE session_id = ? ORDER BY timestamp ASC LIMIT ?",
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
                    timestamp=datetime.fromisoformat(row[4]),
                    health_behavior_data=row[5]  # JSON字符串或None
                ))
            
            return messages
    
    async def clear_messages(self, session_id: str):
        """清空会话的所有消息"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            await db.commit()
    
    async def clear_all_messages(self):
        """清空所有消息"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM messages")
            await db.commit()
    
    async def get_recent_messages(self, limit: int = 20) -> List[Message]:
        """获取全局最近的消息列表"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, session_id, content, is_user, timestamp, health_behavior_data FROM messages ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            rows = await cursor.fetchall()
            
            messages = []
            for row in rows:
                messages.append(Message(
                    id=row[0],
                    session_id=row[1],
                    content=row[2],
                    is_user=bool(row[3]),
                    timestamp=datetime.fromisoformat(row[4]),
                    health_behavior_data=row[5]  # JSON字符串或None
                ))
            
            # 返回时间正序排列（最早的在前面）
            return list(reversed(messages))
    
    async def update_message_health_behavior(self, message_id: str, health_behavior_data: dict) -> bool:
        """更新消息的健康行为数据"""
        health_behavior_json = json.dumps(health_behavior_data)
        
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "UPDATE messages SET health_behavior_data = ? WHERE id = ?",
                (health_behavior_json, message_id)
            )
            await db.commit()
            return cursor.rowcount > 0
    
    async def get_all_sessions(self) -> List[str]:
        """获取所有会话ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT DISTINCT session_id FROM messages")
            rows = await cursor.fetchall()
            return [row[0] for row in rows]