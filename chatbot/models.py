from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str

class TransactionsArgs(BaseModel):
    limit: int = Field(5, description="Quantidade de transações mais recentes a retornar. Padrão: 5.", gt=0, le=50)

class ClientArgs(BaseModel):
    pass

class BankSupportInput(BaseModel):
    request: str = Field(
        description="A pergunta, dúvida ou solicitação exata feita pelo usuário sobre o banco."
    )


