from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str

class TransactionsArgs(BaseModel):
    limit: int = Field(5, description="Number of most recent transactions to return. Default: 5.", gt=0, le=50)

class ClientArgs(BaseModel):
    pass

class BankSupportInput(BaseModel):
    request: str = Field(
        description="The exact question, doubt, or request made by the user about the bank."
    )


