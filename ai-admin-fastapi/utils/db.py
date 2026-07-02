# 导入数据库驱动和工具
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.settings import DB_CONFIG 

# 定义Base
Base = declarative_base()

# 拼接数据库连接地址
db_url = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}/{DB_CONFIG['database']}?charset={DB_CONFIG['charset']}"
)

# 创建数据库引擎（相当于数据库“总开关”）
engine = create_engine(db_url)

# 创建会话工厂（用来操作数据库的“把手”）
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# 数据库连接依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()