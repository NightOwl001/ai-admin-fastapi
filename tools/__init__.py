from langchain_core.tools import BaseTool

from tools.user_tools import get_user_count, search_users_by_username

ALL_TOOLS: list[BaseTool] = [
    get_user_count,
    search_users_by_username,
]


def get_all_tools() -> list[BaseTool]:
    return ALL_TOOLS
