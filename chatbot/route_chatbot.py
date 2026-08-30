from fastapi import APIRouter, HTTPException, status, Depends
from chatbot.models import ChatRequest
from accounts.models import User
from accounts.auth_model import get_current_user
from .langchain.satoshi_agent import build_agent_executor
from langchain_core.messages import HumanMessage, AIMessage
from .langchain.web_tools import current_user_id


router = APIRouter(
    prefix="/api",
    tags=["Chatbot"]
)

agent_executor = build_agent_executor()

# Em produção, salvar isso em um banco de dados usando o current_user.id.
SESSION_HISTORY = {}

@router.post("/chatbot-text", status_code=status.HTTP_200_OK)
async def chatbot_local(request: ChatRequest, current_user: User = Depends(get_current_user)):

    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="A message is required."
        )

    # Recuperando msg na memo
    if current_user.id not in SESSION_HISTORY:
        SESSION_HISTORY[current_user.id] = []
    chat_history = SESSION_HISTORY[current_user.id]

    uid_token = current_user_id.set(current_user.id)

    try:
        result = agent_executor.invoke(
            {"input": request.message, "chat_history": chat_history}
        )
        bot_reply = result["output"]

        if "sucesso" in bot_reply.lower() or "cancelada" in bot_reply.lower():
            SESSION_HISTORY[current_user.id] = []
        else:
            chat_history.append(HumanMessage(content=request.message))
            chat_history.append(AIMessage(content=bot_reply))

        return {"response": bot_reply}

    except Exception as e:
        print(f"[Chatbot Error]: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing the response in the Artificial Intelligence engine."
        )
    finally:
        current_user_id.reset(uid_token)

