from sqlalchemy.orm import Session
from datetime import timedelta
from dao.user_dao import create_user,get_user_by_username,get_user_list_with_page
from utils.jwt_util import hash_password,verify_password,create_access_token
from utils.response import fail_response,success_response
from utils.log_util import logger
from model.schema import UserRegister, UserLogin, UserResponse

def register_service(db:Session,user: UserRegister):
    logger.info(f"用户注册请求: username={user.username}")
    # 1.校验用户名是否存在
    exist_user = get_user_by_username(db,user.username)
    if exist_user:
        logger.warning(f"注册失败,用户名已存在:{user.username}")
        return fail_response(msg="用户名已存在")
    
    # 2.密码加密
    hashed_pwd = hash_password(user.password)

    # 3.创建用户
    new_user = create_user(db,user,hashed_pwd)
    user_response = UserResponse.from_orm(new_user)
    logger.info(f"用户注册成功: username={user.username},id={new_user.id}")
    return success_response(data=user_response,msg="注册成功")

def login_service(db:Session,user:UserLogin):
    logger.info(f"用户登录请求: username={user.username}")
    # 1.校验用户是否存在
    db_user = get_user_by_username(db,user.username)
    if not db_user:
        logger.warning(f"登录失败,用户不存在: {user.username}")
        return fail_response(msg="用户不存在")

    # 2.校验密码
    if not verify_password(user.password,db_user.password):
        logger.warning(f"登录失败,密码错误:{user.username}")
        return fail_response(msg="密码错误")

    # 3.生成JWT令牌
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=60*24)
    )
    logger.info(f"用户登录成功: username={user.username}")
    return success_response(
        data={"access_token": access_token,"token_type": "bearer"},
        msg="登录成功"
    )

def get_user_list_service(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    username: str = None
):
    logger.info(f"用户列表查询请求: page={page},page_size={page_size},username={username}")
    # 调用DAO层分页查询
    user_list,total = get_user_list_with_page(db,page,page_size,username)

    # 封装分页数据
    data = {
        "list": user_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }
    return success_response(data=data,msg="查询成功")