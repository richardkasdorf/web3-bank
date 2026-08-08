from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.utils.uuid import uuid7
from langgraph.types import Command
from web_tools import internet_search


class ResearchAgent:

    def __init__(self):

        system_prompt = """
            # INSTRUÇÕES CRÍTICAS DE OPERAÇÃO
                Você é um leitor factual de dados. Você não pensa, não assume e não calcula. Você deve sempre responder em português.
            ## REGRAS ABSOLUTAS DE RESPOSTA:
                1. Copie EXATAMENTE o número/valor retornado pela ferramenta `internet_search`.
                2. Se a ferramenta contiver o texto "64940", você deve responder "64940".
                3. É PROIBIDO usar qualquer valor da sua memória.
                4. É PROIBIDO inventar números que não estão no texto da busca.
                5. Se o dado não estiver explicitamente no texto recebido, responda apenas: "Dados não encontrados na busca".
            ## FORMATO DA RESPOSTA:
                Responda em apenas uma linha curta, direto ao ponto. Exemplo: "O valor encontrado na pesquisa é de X USD."
        """

        self.agent = create_deep_agent(
            model = init_chat_model(model="qwen2.5:3b", model_provider="ollama", temperature=0, num_ctx=2048),
            tools=[internet_search],
            system_prompt=system_prompt,
            interrupt_on={"internet_search": True},
            checkpointer=MemorySaver(),
        )



    def ask(self, question: str) -> str:

        config = {"configurable": {"thread_id": str(uuid7())}}

        print("🤖 AI search...")

        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": question}]}, 
            config=config, 
            version="v2",
        )

        # Check if execution was interrupted
        if result.interrupts:

            print("\n🚦  SECURE ALERT: Agent wants your permission to use a web search tool.")
            # Extract interrupt information
            interrupt_value = result.interrupts[0].value  
            action_requests = interrupt_value["action_requests"]
            review_configs = interrupt_value["review_configs"]

            # Create a lookup map from tool name to review config
            config_map = {cfg["action_name"]: cfg for cfg in review_configs}

            # Display the pending actions to the user
            for action in action_requests:
                review_config = config_map[action["name"]]
                print(f"Requested Tool: {action['name']}")
                print(f"AI Arguments sent to Web Search: {action['args']}")
                print(f"Allowed Decisions: {review_config['allowed_decisions']}")

            # Get user decisions (one per action_request, in order)
            decisions = ""
            while action not in ["approve", "reject"]:
                action = input("\nDo you authorize this web search? Type 'approve' for YES or 'reject' for NO.: ").strip().lower()

            if action == "approve":
                print("🤖 Searching Tavily with your authorization...")
                decisions = [{
                    "type": "approve",
                    "message": "User approved web search manually.",
                }]
            else:
                print("🚫 Search rejected by the user. The agent will attempt to respond without an internet connection....")
                decisions = [{
                    "type": "reject",
                    "message": "User rejected the web search. Do not use the tool.",
                }]

            # Resume execution with decisions
            result = self.agent.invoke(
                Command(resume={"decisions": decisions}),
                config=config,
                version="v2"
            )

        print(result["messages"][-1].content)

        # warnings.filterwarnings("ignore", category=UserWarning)

        # raw_content = result.value["messages"][-1].content
        # if isinstance(raw_content, list):
        #     clean_text = ""

        #     for block in raw_content:

        #         if isinstance(block, dict) and "text" in block:
        #             clean_text += block["text"]

        #         elif isinstance(block, str):
        #             clean_text += block
                    
        #     print("\n🤖 Final response:")
        #     print(clean_text.strip())

        # else:
        #     print("\n🤖 Final response:")
        #     print(str(raw_content).strip())




if __name__ == "__main__":
    my_agent = ResearchAgent()
    question = "Me resuma o que é stablecoin."
    response = my_agent.ask(question)



