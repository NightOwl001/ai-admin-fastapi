from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / ".env")

# 数据库配置
DB_CONFIG ={
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_DATABASE"),
    "charset": os.getenv("DB_CHARSET","utf8mb4")
}

# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", "").strip()
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

# 项目运行配置
APP_HOST = "127.0.0.1"
APP_PORT = 8000

# LLM / Agent 配置
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "").strip()
SILICONFLOW_BASE_URL = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
SILICONFLOW_MODEL = os.getenv("SILICONFLOW_MODEL", "deepseek-ai/DeepSeek-V4-Flash")
AGENT_TOOL_TIMEOUT = int(os.getenv("AGENT_TOOL_TIMEOUT", "5"))
AGENT_MAX_KEYWORD_LEN = int(os.getenv("AGENT_MAX_KEYWORD_LEN", "32"))
