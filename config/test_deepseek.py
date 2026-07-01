import os
from openai import OpenAI
from dotenv import load_dotenv

# 指定 .env 文件的绝对路径（根据你的项目路径修改）
load_dotenv("E:/backend/codepython_backend/ai-admin-fastapi/config/.env")

# 或者使用相对路径（如果你的脚本在项目根目录运行）
# load_dotenv(".env")  # 默认就是加载 .env 文件，如果你确认 .env 存在且内容正确，这行可以省略

print("当前工作目录:", os.getcwd())
api_key = os.getenv("DEEPSEEK_API_KEY")
print(f"API Key 前8位: {api_key[:8] if api_key else '未找到'}")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",  # 或 deepseek-v4-pro
    messages=[{"role": "user", "content": "你好"}]
)

print(response.choices[0].message.content)