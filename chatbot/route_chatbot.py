from fastapi import APIRouter, HTTPException, status, Depends
from chatbot.models import ChatRequest
from accounts.models import User
from accounts.auth_model import get_current_user
from .langchain.satoshi_agent import agent
from langchain_core.messages import HumanMessage, AIMessage
from .langchain.web_tools import current_user_id
import traceback


router = APIRouter(
    prefix="/api",
    tags=["Chatbot"]
)

# OBS TO DO: save this to a database using `current_user.id`.
SESSION_HISTORY = {}

@router.post("/chatbot-text", status_code=status.HTTP_200_OK)
async def chatbot_local(request: ChatRequest, current_user: User = Depends(get_current_user)):

    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="A message is required."
        )

    if current_user.id not in SESSION_HISTORY:
        SESSION_HISTORY[current_user.id] = []
    chat_history = SESSION_HISTORY[current_user.id]

    uid_token = current_user_id.set(current_user.id)

    try:
        result = agent.invoke(
            {"messages": chat_history[-6:] + [HumanMessage(content=request.message)]}
        )
        for m in result["messages"]:
            m.pretty_print()
        bot_reply = result["messages"][-1].content

        if "sucesso" in bot_reply.lower() or "cancelada" in bot_reply.lower():
            SESSION_HISTORY[current_user.id] = []
        else:
            chat_history.append(HumanMessage(content=request.message))
            chat_history.append(AIMessage(content=bot_reply))

        return {"response": bot_reply}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing the response in the Artificial Intelligence engine."
        )
    finally:
        current_user_id.reset(uid_token)

