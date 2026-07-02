from pydantic import BaseModel, Field, field_validator
from datetime import datetime

# 注册请求体
class UserRegister(BaseModel):
    username: str = Field(
        min_length=2, 
        max_length=32, 
        description="用户名不能为空，长度2-32位"
    )
    password: str = Field(
        min_length=6, 
        max_length=64, 
        description="密码不能为空，长度6-64位"
    )

    #Pydantic V2 正确写法：验证前自动去首尾空格
    @field_validator('username', 'password', mode='before')
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

# 登录请求体（同步修复）
class UserLogin(BaseModel):
    username: str = Field(min_length=2, max_length=32)
    password: str = Field(min_length=6, max_length=64)

    @field_validator('username', 'password', mode='before')
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

# 用户响应体
class UserResponse(BaseModel):
    id: int
    username: str
    create_time: datetime
    class Config:
        from_attributes = True
