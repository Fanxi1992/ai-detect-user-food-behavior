import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# OpenRouter API配置
OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY", 
    "sk-or-v1-your-openrouter-api-key-here"  # 默认值，请在.env文件中设置实际值
)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# 使用的模型（支持结构化输出的模型）
HEALTH_DETECTION_MODEL = "openai/gpt-4o-mini"  # 或者 "openai/gpt-4o-2024-08-06"

# 聊天响应模型
CHAT_MODEL = os.getenv("CHAT_MODEL", "openai/gpt-4o-mini")

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./chatbot.db")