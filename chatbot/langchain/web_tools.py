from typing import Literal
from ddgs import DDGS
from pydantic import BaseModel, Field
import requests
from tavily import TavilyClient
import os
from langchain.tools import tool
from dotenv import load_dotenv


# @tool
# def internet_search(query: str) -> str:
#     """USE ESTA FERRAMENTA PARA QUALQUER PERGUNTA DO USUÁRIO. 
#     Se você não sabe o que significa uma palavra ou tecnologia como 'langgraph', chame esta função imediatamente.
#     """
#     try:
#         with DDGS() as ddgs:
#             results = [r['body'] for r in ddgs.text(query, max_results=3)]
#             return "\n\n".join(results) if results else "Nenhum resultado encontrado."
#     except Exception as e:
#         return f"Falha ao realizar a busca: {str(e)}"


# tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

# @tool
# def internet_search(
#     query: str,
#     max_results: int = 5,
#     topic: Literal["general", "news", "finance"] = "general",
#     include_raw_content: bool = False,
# ):
#     """Run a web search"""
#     return tavily_client.search(
#         query,
#         max_results=max_results,
#         include_raw_content=include_raw_content,
#         topic=topic,
#     )


## ---------------------------------------------------------------------------------------------- ##

load_dotenv()

API_BASE_URL = os.getenv("TRANSFER_API_BASE_URL", "http://localhost:8000")
 
# JWT do usuário autenticado, obtido do seu fluxo de login existente.
# Para os testes via CMD, gere um token (login normal) e cole aqui via .env.
USER_AUTH_TOKEN = os.getenv("USER_AUTH_TOKEN")


class TransferInput(BaseModel):
    amount: float = Field(
        ...,
        description="Valor em USDC a ser transferido. Ex: 10.5",
        gt=0,
    )
    account: str = Field(
        ...,
        description=(
            "Identificador da conta/destinatário informado pelo usuário "
            "(pode ser endereço 0x, e-mail, username, etc. — quem resolve é "
            "o backend via resolve_destination)."
        ),
    )


@tool("transferir_usdc", args_schema=TransferInput)
def agent_transfer(amount: float, account: str) -> str:
    """
    Executa uma transferência de USDC na rede Sepolia (testnet) para a conta
    informada, usando a rota /transactions/transfer já existente no backend.
 
    Use esta ferramenta sempre que o usuário pedir para transferir, enviar ou
    mandar USDC (ou "dinheiro") para uma conta/destinatário específico,
    informando o valor (amount) e a conta de destino (account).
    """
    print("Chamando tool")
    if not USER_AUTH_TOKEN:
        return (
            "Erro: USER_AUTH_TOKEN não configurado. Faça login no seu backend "
            "e defina o JWT no .env antes de tentar transferir."
        )
    print("Autendicação OK!")
    
    payload = {
        "amount": amount,
        "destination": account,
        
    }
    print("Payload carregado")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {USER_AUTH_TOKEN}",
    }
    print("Headers carregado")

    try:
        response = requests.post(
            f"{API_BASE_URL}/transactions/transfer",
            json=payload,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        print(f"Aqui está response: {response}")
        print(f"Aqui está data (Json): {data}")

        return (
            f"Transferência de {amount} USDC para '{account}' iniciada com sucesso "
            f"(destino resolvido: {data.get('resolved_destination')}). "
            f"ID da transação Circle: {data.get('circle_transaction_id')} "
            f"| Estado: {data.get('state')}"
        )
    
    except requests.exceptions.HTTPError as e:
        # A API já retorna detail com mensagens claras (404, 400, 502)
        try:
            detail = e.response.json().get("detail", e.response.text)
        except ValueError:
            detail = e.response.text
        return f"Falha na transferência: {detail}"

    except requests.exceptions.ConnectionError:
        return (
            f"Não foi possível conectar à API em {API_BASE_URL}. "
            "Verifique se o backend está rodando e se TRANSFER_API_BASE_URL está correto."
        )

    except requests.exceptions.RequestException as e:
        return f"Erro inesperado ao chamar a API de transferência: {str(e)}"
