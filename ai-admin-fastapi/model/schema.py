from pydantic import BaseModel
from datetime import datetime

# 注册请求体
class UserRegister(BaseModel):
    username: str
    password: str

# 登录请求体
class UserLogin(BaseModel):
    username: str
    password: str

# 用户响应体
class UserResponse(BaseModel):
    id: int
    username: str
    create_time: datetime

    class Config:
        from_attributes = True