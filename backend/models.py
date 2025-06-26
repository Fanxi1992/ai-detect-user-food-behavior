from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    message: str
    session_id: str
    timestamp: datetime

class Message(BaseModel):
    content: str
    is_user: bool
    timestamp: datetime

class StreamChunk(BaseModel):
    content: str
    done: bool = False