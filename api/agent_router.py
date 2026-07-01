from fastapi import APIRouter, Depends
from utils.jwt_util import get_current_user
from model.entity import User
from model.schema import AgentChatRequest
from service.agent_service import chat_service

router = APIRouter(prefix="/api/agent", tags=["AI Agent"])

@router.post("/chat", summary="Agent 对话式业务问答")
def agent_chat(
    req: AgentChatRequest,
    current_user: User = Depends(get_current_user)
):
    return chat_service(req.question)