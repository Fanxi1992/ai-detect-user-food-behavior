from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import json
import uuid
from datetime import datetime
from typing import List, Optional

from database import Database, Message as DBMessage
from models import ChatRequest, ChatResponse, Message

app = FastAPI(title="AI Chatbot API", version="1.0.0")

# CORS设置，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
db = Database()

@app.on_event("startup")
async def startup_event():
    await db.init_db()

@app.get("/")
async def root():
    return {"message": "AI Chatbot API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """非流式聊天接口"""
    try:
        # 保存用户消息
        user_message = await db.save_message(
            session_id=request.session_id,
            content=request.message,
            is_user=True
        )
        
        # 模拟AI回复（后续替换为真实LLM调用）
        ai_response = f"收到您的消息：{request.message}。这是一个模拟的AI回复。"
        
        # 保存AI回复
        ai_message = await db.save_message(
            session_id=request.session_id,
            content=ai_response,
            is_user=False
        )
        
        return ChatResponse(
            message=ai_response,
            session_id=request.session_id,
            timestamp=ai_message.timestamp
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """流式聊天接口"""
    try:
        # 保存用户消息
        await db.save_message(
            session_id=request.session_id,
            content=request.message,
            is_user=True
        )
        
        async def generate_stream():
            # 模拟AI流式回复
            ai_responses = [
                "这是一个",
                "流式的",
                "AI回复。",
                "每个部分",
                "会逐步",
                "发送给",
                "前端。",
                f"\n\n您刚才说：{request.message}",
                "\n\n我理解了您的问题，",
                "让我来详细回答..."
            ]
            
            full_response = ""
            for chunk in ai_responses:
                full_response += chunk
                # 发送数据块
                yield f"data: {json.dumps({'content': chunk, 'done': False})}\n\n"
                # 模拟处理延迟
                await asyncio.sleep(0.2)
            
            # 保存完整的AI回复
            await db.save_message(
                session_id=request.session_id,
                content=full_response,
                is_user=False
            )
            
            # 发送结束标志
            yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/history/{session_id}")
async def get_chat_history(session_id: str) -> List[Message]:
    """获取聊天历史"""
    try:
        messages = await db.get_messages(session_id)
        return [
            Message(
                content=msg.content,
                is_user=msg.is_user,
                timestamp=msg.timestamp
            )
            for msg in messages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/chat/history/{session_id}")
async def clear_chat_history(session_id: str):
    """清空聊天历史"""
    try:
        await db.clear_messages(session_id)
        return {"message": "Chat history cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)