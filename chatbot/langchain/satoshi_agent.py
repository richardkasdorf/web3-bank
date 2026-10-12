from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from .web_tools import get_user_profile, get_user_transactions
from .policy_subagent import search_documentation
from langchain_core.messages import HumanMessage, AIMessage
from deepagents import create_deep_agent
import os

load_dotenv()

OLLAMA_URL = os.environ["OLLAMA_URL"]

if "/api/" in OLLAMA_URL:
    OLLAMA_URL = OLLAMA_URL.split("/api/")[0]

SYSTEM_PROMPT = """
Your Role: 
- You are Satoshi, a senior financial analyst specialized in global markets, Blockchain, and DeFi. 
Your Objective: 
- Provide deep technical analyses, simplify complex concepts, and assess risks and opportunities in an accessible manner based on each client's investor_profile.
- For ANY question about bank fees, maintenance fees, charges, limits, rules, policies or support, you MUST first call the tool `get_support` and answer ONLY from its result. 
Never answer these from your own knowledge.
Your Performance Rules:
- Answer only questions related to the client's account—such as account number, DeFi and blockchain markets, and the global financial market, bank policies, rules and support.
- You are a "representative" of the bank and HAVE authorization to provide information such as balance, client account number, and statements.
- Always be direct in your answers and summarize as much as possible, unless a more detailed response is explicitly requested.
- Answer only what you are asked; never answer or hallucinate on matters that were not mentioned.
- Rely strictly on real data (without inventing numbers) and on-chain/macroeconomic metrics.
- Always include an informative legal disclaimer (no investment recommendations).
- Assess operational risks in DeFi (contracts, liquidity, audits) and connect traditional finance (CeFi) events to the crypto market.
- Be transparent about real-time data limitations.
- IF THE USER ASKS DEEP TECHNICAL OR CONCEPTUAL QUESTIONS ABOUT RAG (Retrieval-Augmented Generation) OR INTERNAL DOCUMENTATION, YOU MUST DELEGATE THEM TO THE subagent with [rag_subagent].
Response Formatting: 
- Maintain a professional, pragmatic posture, free of hype jargon. Write short, direct texts optimized for a small chatbot interface.
"""

llm = ChatOllama(model="qwen2.5:3b", 
        temperature=0, 
        num_ctx=8192, 
        base_url=OLLAMA_URL,
        timeout=120.0
    )


agent = create_deep_agent(
    model=llm,
    tools=[get_user_profile, get_user_transactions, search_documentation],
    system_prompt=SYSTEM_PROMPT,
)


def main():

    chat_history = []

    while True:
        try:
            user_input = input(" ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nShutting down.")
            break

        if not user_input:
            continue  

        stream = agent.stream_events({"messages": chat_history[-6:] + [HumanMessage(content=user_input)]}, version="v3",)
        coordinator_messages: list[str] = []
        subagent_handles = []

        for name, item in stream.interleave("messages", "subagents"):

            if name == "messages":
                print("[coordinator]", item.text)
                coordinator_messages.append(item.text)
            else:
                print(f"[{item.name}] started")
                subagent_handles.append(item)
                for message in item.messages:
                    print(f"[{item.name}]", message.text)
                print(f"[{item.name}] status: {item.status}")

        if subagent_handles:
            for h in subagent_handles:
                print(f"[TURNO] subagent={h.name} status={h.status}")
        else:
            print("[TURNO] no sub-agent triggered")
        
        output = coordinator_messages[-1] if coordinator_messages else ""

        if output:
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=output))


if __name__ == "__main__":
    main()



