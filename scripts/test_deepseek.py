import os
from openai import OpenAI
from dotenv import load_dotenv

# 指定 .env 文件的完整路径
load_dotenv("E:/backend/codepython_backend/ai-admin-fastapi/config/.env")

api_key = os.getenv("SILICONFLOW_API_KEY")
print(f"API Key 前8位: {api_key[:8] if api_key else '未找到'}")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V4-Flash",
    messages=[{"role": "user", "content": "你好"}]
)

print(response.choices[0].message.content)