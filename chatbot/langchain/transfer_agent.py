from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from web_tools import agent_transfer
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent



load_dotenv()

SYSTEM_PROMPT = """Você é um assistente que ajuda a executar transferências de USDC
na rede Sepolia (testnet) através da ferramenta disponível.
 
Regras:
- Sempre que o usuário pedir uma transferência, extraia claramente:
  - amount: o valor numérico em USDC
  - account: o endereço de destino (começa com 0x)
- Se algum dos dois dados estiver faltando ou for ambíguo, pergunte ao usuário
  antes de chamar a ferramenta. Nunca invente valores ou endereços.
- Depois de chamar a ferramenta, responda ao usuário de forma clara e direta
  com o resultado (sucesso, hash da transação, ou erro).
- Para qualquer outro assunto que não seja transferência, responda normalmente
  como um assistente útil.
"""


def build_agent_executor() -> AgentExecutor:
    
    llm = ChatOllama(model="qwen2.5:3b", model_provider="ollama", temperature=0, num_ctx=2048)

    tools = [agent_transfer]
 
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

print("Agente criado")


def main():

        print("Iniciando inputs.")
    
        executor = build_agent_executor()
        chat_history = []
    
        print("=== Agente de Transferência USDC (Sepolia) ===")
        print("Exemplo: 'transfere 10 usdc para 0x1234...abcd'")
        print("Digite 'sair' para encerrar.\n")
    
        while True:
            try:
                user_input = input("Você: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nEncerrando.")
                break
    
            if not user_input:
                continue
            if user_input.lower() in ("sair", "exit", "quit"):
                print("Encerrando.")
                break

            print("Chamando agente")
            result = executor.invoke(
                {"input": user_input, "chat_history": chat_history}
            )
            output = result["output"]
    
            print(f"Agente: {output}\n")
    
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=output))


if __name__ == "__main__":
    main()



