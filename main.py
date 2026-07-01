from fastapi import FastAPI
from utils.db import engine,Base
from model import entity
from api.user_router import router as user_router
from utils.exception_handler import register_exception_handlers
from utils.log_util import logger
from api.agent_router import router as agent_router

# 自动创建数据库表（核心）
entity.Base.metadata.create_all(bind=engine)

# 创建FastAPI实例
app = FastAPI(title="AI_ADMIN_project",version="1.0")

# 1.注册全局异常处理器
register_exception_handlers(app)

# 2.注册路由
app.include_router(user_router)
app.include_router(agent_router)

# 测试接口
@app.get("/",summary="项目根目录")
def root():
    logger.info("访问根路径")
    return {"code": 200,"msg": "AI_ADMIN_project项目启动成功!访问/docs查看接口文档"}

# 启动日志
logger.info("FastAPI项目启动成功!")