# 导入数据库基类和字段类型
from sqlalchemy import Column,Integer,String,DateTime
from datetime import datetime
from utils.db import Base

# 用户表模型
class User(Base):
    __tablename__ = "user" #表名

    id = Column(Integer,primary_key=True,autoincrement=True,comment="主键ID")
    username = Column(String(50),unique=True,nullable=False,comment="用户名")
    password = Column(String(255),nullable=False,comment="加密后的密码")
    create_time = Column(DateTime,default=datetime.now,comment="创建时间")
