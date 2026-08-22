

# LangChain Tools

Organização de ferramentas e funções utilitárias desativadas ou guardadas para referência futura.

## 🔍 Ferramentas de Busca na Internet

### DuckDuckGo Search (DDGS)
Ferramenta simples e gratuita para buscas textuais rápidas.

```python
from ddgs import DDGS

@tool
def internet_search(query: str) -> str:
    """USE ESTA FERRAMENTA PARA QUALQUER PERGUNTA DO USUÁRIO. 
    Se você não sabe o que significa uma palavra ou tecnologia como 'langgraph', chame esta função imediatamente.
    """
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n\n".join(results) if results else "Nenhum resultado encontrado."
    except Exception as e:
        return f"Falha ao realizar a busca: {str(e)}"
```

### Tavily Search API
Ferramenta avançada de busca otimizada para LLMs, com suporte a tópicos e conteúdos brutos.

```python
from typing import Literal
from tavily import TavilyClient

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

@tool
def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )
```

---

## 💸 Ferramentas de Transação (Web3 / API)

### Transferência de USDC (Sepolia Testnet)
Integração com backend para envio de USDC utilizando tokens de autenticação.

```python
from fastapi import Depends

@tool("transferir_usdc", args_schema=TransferArgs)
def agent_transfer(amount: float, account: str, config: RunnableConfig) -> str:
    """Executa uma transferência de USDC na rede Sepolia (testnet) para a conta
    informada, usando a rota /transactions/transfer já existente no backend.
    Use esta ferramenta sempre que o usuário pedir para transferir, enviar ou
    mandar USDC (ou "dinheiro") para uma conta/destinatário específico,
    informando o valor (amount) e a conta de destino (account)."""

    payload = {
        "amount": amount,
        "destination": account,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {USER_AUTH_TOKEN}",
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/transactions/transfer",
            json=payload,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.HTTPError as e:
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
```



# Simple LangChain Services

Classe de serviço para gerenciamento de chat contextualizado, utilizando banco de dados relacional e Ollama para inferência local.

## 🛠️ Configurações e Inicialização

Imports necessários e definição das variáveis de ambiente para conexão com o modelo LLM local (`qwen2.5:3b`).

```python
import os, json
from pathlib import Path
import requests
from db.database import get_db_session
from accounts.models import TransactionLedger, User, Account
from sqlalchemy import or_

OLLAMA_URL = os.getenv('OLLAMA_URL')
MODEL = "qwen2.5:3b"

class ChatbotService:
    def __init__(self):
        ## ----- LOCAL "STUFF" ----- ##
        BASE_DIR = Path("/app/chatbot/data")

        with open(BASE_DIR / "prompt.md", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()
```

---

## 🗄️ Integração com Banco de Dados

Métodos internos para buscar o histórico de transações, o perfil do usuário e os dados da conta corrente na rede blockchain.

```python
    ## ----- DATA BASE INTEGRATION ----- ##
    def _get_user_transactions(self, user_id: int, limit: int = 5):
        db = get_db_session()
        try:
            transactions = (
                db.query(TransactionLedger)
                .filter(
                    or_(
                        TransactionLedger.from_account_id == user_id,
                        TransactionLedger.to_account_id == user_id
                    )
                )
                .order_by(TransactionLedger.id.desc())
                .limit(limit)
                .all()
            )
            tx_list = []
            for tx in transactions:
                direction = "received" if tx.to_account_id == user_id else "sent"
                tx_list.append({
                    "hash": tx.tx_hash,
                    "type": tx.type,
                    "direction": direction,
                    "amount": float(tx.amount) if tx.amount is not None else "N/A",
                    "data": tx.created_at.strftime('%Y-%m-%d %H:%M') if hasattr(tx, 'created_at') else "N/A"
                })
            return tx_list
        except Exception as e:
            print(f"[Database Neon Error]: {e}")
            return []
        finally:
            db.close()

    def _get_user_profile(self, user_id: int):
        db = get_db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"name": "Client", "investor_profile": "Investor profile", "email": "N/A"}

            return {
                "name": user.full_name,
                "email": user.email,
                "investor_profile": user.investor_profile
            }
        except Exception as e:
            print(f"[Database Neon Error - profile]: {e}")
            return {"name": "Client", "investor_profile": "Investor profile", "email": "N/A"}
        finally:
            db.close()

    def _get_user_account(self, user_id: int):
        db = get_db_session()
        try:
            account = db.query(Account).filter(Account.user_id == user_id).first()
            if not account:
                return {"balance": 0.0, "account_number": user_id, "blockchain": "N/A"}

            return {
                "balance": float(account.balance) if account.balance is not None else 0.0,
                "account_number": account.user_id,
                "blockchain": account.blockchain
            }
        except Exception as e:
            print(f"[Database Neon Error - profile]: {e}")
            return {"balance": 0.0, "account_number": user_id, "blockchain": "N/A"}
        finally:
            db.close()
```

---

## 🤖 Geração de Resposta da IA

Lógica de detecção de intenção por palavras-chave financeiras para injeção dinâmica de contexto no prompt enviado ao Ollama.

```python
    ## ----- AI RESPONSE ----- ##
    def generate_reply(self, user_id: int, user_message: str) -> str:
        msg = user_message.lower()

        financial_keywords = ["saldo", "balance", "transaction", "transação", "sent", "enviei",
                            "received", "recebi", "extrato", "money", "dinheiro", "valor", 
                            "perfil", "perfil de risco", "risk profile", "blockchain", "numero conta",
                            "account number"]

        needs_context = any(k in msg for k in financial_keywords)

        if needs_context:
            transactions = self._get_user_transactions(user_id)
            user_profile = self._get_user_profile(user_id)
            account = self._get_user_account(user_id)

            context = (
                f"Nome do cliente (client name): {user_profile['name']}. Perfil de investidor: {user_profile['investor_profile']}.\n"
                f"Saldo atual (balance): {account['balance']} USDC na rede {account['blockchain']}.\n"
                f"Número da conta (account number): {account['account_number']}.\n"
                f"Últimas transações (transactions): {json.dumps(transactions, ensure_ascii=False)}"
            )

        else:
            context = "No financial data needed for this message."

        prompt = f"""
        {self.system_prompt}

        CLIENT CONTEXT:
        {context}

        Message: {msg}
        """

        try:
            a = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=120)
            a.raise_for_status()
            return a.json().get('response', "Sorry, I couldn't generate a response.")
        except requests.exceptions.RequestException as e:
            print(f"[Ollama Error]: {e}")
            return "Sorry, i don't know the answer for your question. But i'm in constantly training."
```
