import os
from openai import OpenAI
from typing import AsyncGenerator, List, Dict, Any
import asyncio
import json
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class OpenRouterService:
    def __init__(self):
        # 从环境变量获取API密钥，如果没有则使用占位符
        self.api_key = os.getenv("OPENROUTER_API_KEY", "your-openrouter-api-key-here")
        
        # 初始化OpenAI客户端，指向OpenRouter
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        
        # 默认模型（可以通过环境变量自定义）
        self.default_model = os.getenv("DEFAULT_MODEL", "openai/gpt-4o-mini")  # 使用更经济的模型
        
    async def chat_completion_stream(
        self, 
        messages: List[Dict[str, str]], 
        model: str = None
    ) -> AsyncGenerator[str, None]:
        """
        流式聊天完成
        """
        if not model:
            model = self.default_model
            
        try:
            # 创建流式聊天完成
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                temperature=0.7,
                max_tokens=1000,
            )
            
            # 逐个处理流式响应
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    yield content
                    # 添加小延迟以模拟真实的流式体验
                    await asyncio.sleep(0.01)
                    
        except Exception as e:
            error_message = f"OpenRouter API调用失败: {str(e)}"
            print(f"Error: {error_message}")
            
            # 如果API调用失败，返回错误信息
            if "api_key" in str(e).lower():
                error_message = "请配置正确的OPENROUTER_API_KEY环境变量"
            
            yield f"❌ {error_message}"
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str = None
    ) -> str:
        """
        非流式聊天完成
        """
        if not model:
            model = self.default_model
            
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            error_message = f"OpenRouter API调用失败: {str(e)}"
            print(f"Error: {error_message}")
            
            if "api_key" in str(e).lower():
                error_message = "请配置正确的OPENROUTER_API_KEY环境变量"
                
            return f"❌ {error_message}"
    
    def format_messages(self, conversation_history: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        将对话历史格式化为OpenAI消息格式
        """
        messages = []
        
        # 添加系统提示
        messages.append({
            "role": "system",
            "content": "你是一个helpful、friendly、knowledgeable的AI助手。请用中文回答用户的问题，保持回答简洁明了。"
        })
        
        # 添加对话历史
        for msg in conversation_history:
            role = "user" if msg.get("is_user", True) else "assistant"
            messages.append({
                "role": role,
                "content": msg.get("content", "")
            })
        
        return messages
    
    def is_api_key_configured(self) -> bool:
        """
        检查API密钥是否已配置
        """
        return self.api_key and self.api_key != "your-openrouter-api-key-here"