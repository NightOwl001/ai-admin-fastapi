from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

from config.settings import AGENT_MAX_KEYWORD_LEN, AGENT_TOOL_TIMEOUT

TOOL_TIMEOUT_SECONDS = AGENT_TOOL_TIMEOUT
MAX_KEYWORD_LEN = AGENT_MAX_KEYWORD_LEN


def run_with_timeout(func, *args, **kwargs) -> str:
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(func, *args, **kwargs)
        try:
            return future.result(timeout=TOOL_TIMEOUT_SECONDS)
        except FuturesTimeoutError:
            return f"工具调用超时（超过 {TOOL_TIMEOUT_SECONDS} 秒），请稍后重试"
        except Exception as e:
            return f"工具执行异常：{str(e)}"


def validate_search_keyword(keyword: str) -> tuple[str | None, str | None]:
    if keyword is None or not str(keyword).strip():
        return "参数错误：搜索关键词不能为空", None
    cleaned = str(keyword).strip()
    if len(cleaned) > MAX_KEYWORD_LEN:
        return f"参数错误：搜索关键词长度不能超过 {MAX_KEYWORD_LEN} 位", None
    return None, cleaned
