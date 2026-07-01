from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from utils.response import fail_response
from utils.log_util import logger

def register_exception_handlers(app: FastAPI):
    # 处理FastAPI自带的HTTP异常
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request,exc: HTTPException):
        logger.error(f"HTTP异常: {exc.detail}")
        return fail_response(msg=exc.detail,code=exc.status_code)

    # 处理数据库异常
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request,exc: SQLAlchemyError):
        logger.error(f"数据库异常: {str(exc)}")
        return fail_response(msg="数据库操作失败",code=500)

    # 处理所有其他未捕获的异常
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request,exc: Exception):
        logger.error(f"系统异常: {str(exc)}",exc_info=True)
        return fail_response(msg="服务器内部错误",code=500)