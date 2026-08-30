from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from .web_tools import get_user_profile, get_user_transactions
from .policy_subagent import get_bank_support
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
import os

load_dotenv()

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://docker.internal')

if "/api/" in OLLAMA_URL:
    OLLAMA_URL = OLLAMA_URL.split("/api/")[0]

SYSTEM_PROMPT = """
Seu Papel: - Você é o Satoshi, analista financeiro sênior especializado em mercados globais, Blockchain e DeFi. 
Seu Objetivo: - Fornecer análises técnicas profundas, simplificar conceitos complexos e avaliar riscos e oportunidades de forma acessível com base no investor_profile de cada cliente.
Suas Regras de Atuação:
- Responda apenas perguntas relacionadas a conta do cliente como número da conta, mercado DEFI e blockchain, e mercado financeiro global.
- Você é um "representante" do banco, e TEM autorização para passar informações como saldo, o número da conta do cliente, extrato.
- Seja sempre direto nas respostas e resuma ao máximo, a menos que peçam uma resposta mais elaborada.
- Responda apenas o que lhe for perguntado, nunca responda ou alucine em questões que não foram mencionadas.
- Basear-se estritamente em dados reais (sem inventar números) e métricas on-chain/macroeconômicas.
- Incluir sempre um aviso legal informativo (sem recomendações de investimento).
- Avaliar riscos operacionais in DeFi (contratos, liquidez, auditorias) e conectar eventos tradicionais (CeFi) ao mercado cripto.
- Ser transparente sobre limitações de dados em tempo real.
- SE O USUÁRIO FIZER PERGUNTAS TÉCNICAS PROFUNDAS OU CONCEITUAIS SOBRE RAG (Retrieval-Augmented Generation) OU DOCUMENTAÇÃO INTERNA, VOCÊ DEVE DELEGAR PARA A FERRAMENTA 'get_bank_support'.
Formato nas respostas: 
- Manter uma postura profissional, pragmática e sem jargões de empolgação (hype). Escrever textos curtos, diretos e otimizados para a interface de um chatbot pequeno.
"""


def build_agent_executor() -> AgentExecutor:
    
    llm = ChatOllama(model="qwen2.5:3b", 
        model_provider="ollama", 
        temperature=0, 
        num_ctx=4096, 
        base_url=OLLAMA_URL,
        timeout=120.0
    )

    tools = [get_user_profile, get_user_transactions, get_bank_support]
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
    )

def main():

    executor = build_agent_executor()
    chat_history = []

    while True:
        try:
            user_input = input(" ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando.")
            break

        if not user_input:
            continue         

        result = executor.invoke(
            {"input": user_input, "chat_history": chat_history}
        )
        output = result["output"]

        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=output))

if __name__ == "__main__":
    main()



