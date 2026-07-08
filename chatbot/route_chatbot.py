from fastapi import APIRouter, HTTPException, status
from chatbot.models import ChatRequest
from chatbot.services import ChatbotService


router = APIRouter(
    prefix="/api",
    tags=["Chatbot"]
)

chatbot_service = ChatbotService()

@router.post("/chatbot-text", status_code=status.HTTP_200_OK)
async def chat_with_gpt(data: ChatRequest):

    if not data.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="A mensagem não pode estar vazia."
        )

    try:
        bot_reply = chatbot_service.generate_reply(data.message)
        return {"reply": bot_reply}

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
