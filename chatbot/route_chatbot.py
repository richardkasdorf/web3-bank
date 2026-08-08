from fastapi import APIRouter, HTTPException, status, Depends
from chatbot.models import ChatRequest
from chatbot.services import ChatbotService
from accounts.models import User
from accounts.auth_model import get_current_user


router = APIRouter(
    prefix="/api",
    tags=["Chatbot"]
)

chatbot_service = ChatbotService()

@router.post("/chatbot-text", status_code=status.HTTP_200_OK)
async def chatbot_local(request: ChatRequest, current_user: User = Depends(get_current_user)):

    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="A mensagem não pode estar vazia."
        )

    try:
        bot_reply = chatbot_service.generate_reply(current_user.id, request.message)
        return {"response": bot_reply}

    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(val_err)
        )
    except Exception as e:
        print(f"[Chatbot Error]: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar a resposta no motor de Inteligência Artificial."
        )
