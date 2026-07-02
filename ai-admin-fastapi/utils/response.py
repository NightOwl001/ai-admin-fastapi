from typing import Any,Optional
from fastapi.responses import JSONResponse

def success_response(data: Any = None, msg: str = "操作成功", code: int = 200) -> JSONResponse:
    return JSONResponse(
        status_code=code,
        content={
            "code": code,
            "msg": msg,
            "data": data
        }
    )

def fail_response(msg: str = "操作失败",code: int = 400,data: Optional[Any] = None) -> JSONResponse:
    return JSONResponse(
        status_code=code,
        content={
            "code": code,
            "msg": msg,
            "data": data
        }
    )
