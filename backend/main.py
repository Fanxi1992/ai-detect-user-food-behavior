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
from openrouter_service import OpenRouterService

app = FastAPI(title="AI Chatbot API", version="1.0.0")

# CORS设置，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库和OpenRouter服务
db = Database()
openrouter = OpenRouterService()

@app.on_event("startup")
async def startup_event():
    await db.init_db()

@app.get("/")
async def root():
    return {"message": "AI Chatbot API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/api/config")
async def config_check():
    """检查配置状态"""
    return {
        "openrouter_configured": openrouter.is_api_key_configured(),
        "default_model": openrouter.default_model,
        "timestamp": datetime.now()
    }

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
        
        # 获取对话历史
        history = await db.get_messages(request.session_id, limit=10)
        
        # 格式化消息给OpenRouter
        messages = openrouter.format_messages([
            {"content": msg.content, "is_user": msg.is_user} 
            for msg in history[:-1]  # 排除刚添加的用户消息
        ])
        messages.append({"role": "user", "content": request.message})
        
        # 调用OpenRouter获取AI回复
        ai_response = await openrouter.chat_completion(messages)
        
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
            try:
                # 获取对话历史
                history = await db.get_messages(request.session_id, limit=10)
                
                # 格式化消息给OpenRouter (排除刚添加的用户消息)
                messages = openrouter.format_messages([
                    {"content": msg.content, "is_user": msg.is_user} 
                    for msg in history[:-1]
                ])
                messages.append({"role": "user", "content": request.message})
                
                # 检查API密钥是否配置
                if not openrouter.is_api_key_configured():
                    error_msg = "⚠️ 请配置OPENROUTER_API_KEY环境变量以使用真实的AI模型"
                    yield f"data: {json.dumps({'content': error_msg, 'done': False})}\n\n"
                    yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
                    
                    # 保存错误消息
                    await db.save_message(
                        session_id=request.session_id,
                        content=error_msg,
                        is_user=False
                    )
                    return
                
                # 调用OpenRouter流式API
                full_response = ""
                async for chunk in openrouter.chat_completion_stream(messages):
                    if chunk:
                        full_response += chunk
                        # 发送数据块
                        yield f"data: {json.dumps({'content': chunk, 'done': False})}\n\n"
                
                # 保存完整的AI回复
                if full_response.strip():
                    await db.save_message(
                        session_id=request.session_id,
                        content=full_response,
                        is_user=False
                    )
                
                # 发送结束标志
                yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
                
            except Exception as stream_error:
                error_message = f"❌ 流式处理错误: {str(stream_error)}"
                yield f"data: {json.dumps({'content': error_message, 'done': False})}\n\n"
                yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
                
                # 保存错误消息
                await db.save_message(
                    session_id=request.session_id,
                    content=error_message,
                    is_user=False
                )
        
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

@app.get("/api/chat/history/recent")
async def get_recent_chat_history(limit: int = 20) -> List[Message]:
    """获取最近的聊天历史（全局）"""
    try:
        messages = await db.get_recent_messages(limit)
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

@app.get("/api/chat/history/{session_id}")
async def get_chat_history(session_id: str) -> List[Message]:
    """获取特定会话的聊天历史"""
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

@app.delete("/api/chat/history/all")
async def clear_all_chat_history():
    """清空所有聊天历史"""
    try:
        await db.clear_all_messages()
        return {"message": "All chat history cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/chat/history/{session_id}")
async def clear_chat_history(session_id: str):
    """清空特定会话的聊天历史"""
    try:
        await db.clear_messages(session_id)
        return {"message": "Chat history cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)