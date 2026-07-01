from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from utils.db import get_db
from model.schema import UserRegister,UserLogin,UserUpdateReq
from service.user_service import register_service,login_service,get_user_list_service,update_user_service, delete_user_service
#新增
from utils.jwt_util import get_current_user
from model.entity import User

router = APIRouter(prefix="/api/user",tags=["用户管理"])

# 注册接口
@router.post("/register",summary="用户注册")
def register(user: UserRegister,db: Session = Depends(get_db)):
    return register_service(db,user)

# 登录接口
@router.post("/login",summary="用户登录")
def login(user: UserLogin,db: Session = Depends(get_db)):
    return login_service(db,user)

# 用户列表接口(升级为分页+条件查询)
@router.get("/list",summary="用户列表(分页+条件查询)")
def user_list(
    db: Session = Depends(get_db),
    page: int = Query(1,ge=1,description="页码,从1开始"),
    page_size: int = Query(10,ge=1,le=100,description="每页条数,1-100"),
    username: str = Query(None,description="用户名模糊查询,可选")
):
    return get_user_list_service(db,page,page_size,username)

#新增
@router.put("/update", summary="修改昵称")
def update_user(
    req: UserUpdateReq,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_user_service(db, current_user, req)

@router.delete("/delete", summary="删除自己的账号")
def delete_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_user_service(db, current_user)