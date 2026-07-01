import jwt
from typing import Optional
from datetime import datetime,timedelta
from passlib.context import CryptContext
from config.settings import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from utils.db import get_db
from model.entity import User

security = HTTPBearer()

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

# 添加获取当前用户的依赖
def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = cred.credentials.strip()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="无效token")
        user = db.query(User).filter(User.username == username, User.is_deleted == False).first()
        if not user:
            raise HTTPException(status_code=401, detail="用户不存在")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="token无效或已过期")

