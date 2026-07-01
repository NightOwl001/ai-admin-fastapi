from langchain_core.tools import tool

from dao.user_dao import get_user_list_with_page
from tools.base import run_with_timeout, validate_search_keyword
from utils.db import SessionLocal
from utils.log_util import logger


def _get_user_count_impl() -> str:
    db = SessionLocal()
    try:
        _, total = get_user_list_with_page(db, page=1, page_size=1, username=None)
        logger.info(f"工具 get_user_count 执行成功，count={total}")
        return f"当前系统共有 {total} 位未删除用户。"
    finally:
        db.close()


def _search_users_by_username_impl(keyword: str) -> str:
    db = SessionLocal()
    try:
        users, total = get_user_list_with_page(db, page=1, page_size=10, username=keyword)
        if total == 0:
            return f"未找到用户名包含「{keyword}」的用户。"
        lines = [f"共找到 {total} 位匹配用户，前 {len(users)} 条："]
        for u in users:
            nickname = u.nickname or "未设置"
            lines.append(f"- ID={u.id}, username={u.username}, nickname={nickname}")
        logger.info(f"工具 search_users_by_username 执行成功，keyword={keyword}, total={total}")
        return "\n".join(lines)
    finally:
        db.close()


@tool
def get_user_count() -> str:
    """查询系统中未删除用户的总数量。无需任何参数。"""
    return run_with_timeout(_get_user_count_impl)


@tool
def search_users_by_username(username: str) -> str:
    """根据用户名关键词进行模糊搜索，返回匹配的用户列表摘要。参数 username 为搜索关键词。"""
    err, keyword = validate_search_keyword(username)
    if err:
        return err
    return run_with_timeout(_search_users_by_username_impl, keyword)
