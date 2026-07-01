from sqlalchemy.orm import Session
from sqlalchemy import or_
from model.entity import User
from model.schema import UserRegister

def create_user(db: Session,user: UserRegister,hashed_pwd:str) -> User:
    """创建用户"""
    db_user = User(username=user.username,password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session,username: str) -> User | None:
    """根据用户名查询用户"""
    return db.query(User).filter(User.is_deleted == False,User.username == username).first()

def get_user_list_with_page(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    username: str = None
)-> tuple[list[User],int]:
    """
    分页+条件查询用户列表
    :param page: 页码(从1开始)
    :param page_size: 每页条数
    :param username: 用户名模糊查询
    :return: 用户列表,总条数
    """
    query = db.query(User).filter(User.is_deleted == False) #修改，只查未删除用户
    #修复1：只有username非空且不是纯空格时才拼接模糊条件
    if username is not None and username.strip() != "":
        #修复2：前后通配符，实现真正的包含模糊查询
        query = query.filter(User.username.like(f"%{username}%"))
    
    offset = (page - 1) * page_size
    total = query.count()
    user_list = query.offset(offset).limit(page_size).all()
    return user_list,total

def update_user_nickname(db: Session, user_id: int, nickname: str) -> User | None:
    """更新用户昵称"""
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if user:
        user.nickname = nickname
        db.commit()
        db.refresh(user)
    return user

def delete_user_by_id(db: Session, user_id: int) -> bool:
    """物理删除用户"""
    user = db.query(User).filter(User.id == user_id,User.is_deleted == False).first()
    if user:
        user.is_deleted = True
        db.commit()
        return True
    return False
