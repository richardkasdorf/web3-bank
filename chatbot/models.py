from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(
        ..., 
        description="A mensagem de texto enviada pelo usuário no chatbot",
        example="Qual é o meu saldo atual em USDC?"
    )


