import jwt
from typing import Optional
from datetime import datetime,timedelta
from passlib.context import CryptContext
from config.settings import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES


# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password: str) -> str:
    """密码加密"""
    return pwd_context.hash(password)

def verify_password(plain_password: str,hashed_password: str) -> bool:
    """密码效验"""
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict,expires_delta: Optional[timedelta] = None) -> str:
    """生成JWT令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt