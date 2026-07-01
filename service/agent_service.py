from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config.settings import (
    SILICONFLOW_API_KEY,
    SILICONFLOW_BASE_URL,
    SILICONFLOW_MODEL,
)
from tools import get_all_tools
from utils.log_util import logger
from utils.response import fail_response, success_response

SYSTEM_PROMPT = "你是一个用户管理助手，可以调用工具查询用户相关数据。请根据工具返回结果用中文简洁回答。"

_agent_executor: AgentExecutor | None = None


def _build_agent_executor() -> AgentExecutor:
    llm = ChatOpenAI(
        base_url=SILICONFLOW_BASE_URL,
        model=SILICONFLOW_MODEL,
        api_key=SILICONFLOW_API_KEY,
        temperature=0.1,
    )
    tools = get_all_tools()
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)


def get_agent_executor() -> AgentExecutor:
    global _agent_executor
    if _agent_executor is None:
        _agent_executor = _build_agent_executor()
    return _agent_executor


def chat_service(question: str):
    logger.info(f"Agent 对话请求: question={question}")
    if not SILICONFLOW_API_KEY:
        return fail_response(msg="未配置 SILICONFLOW_API_KEY，请在 config/.env 中设置")
    try:
        result = get_agent_executor().invoke({"input": question})
        answer = result.get("output", "")
        logger.info(f"Agent 对话成功: answer={answer[:100]}")
        return success_response(data={"answer": answer}, msg="对话成功")
    except Exception as e:
        logger.error(f"Agent 对话失败: {e}")
        return fail_response(msg=f"Agent 对话失败：{str(e)}")
