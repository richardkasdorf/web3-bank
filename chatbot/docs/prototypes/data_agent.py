import getpass
import os, io, csv
from dotenv import load_dotenv
from e2b import Sandbox
from langchain_e2b import E2BSandbox
from pathlib import Path
from langchain.tools import tool
from slack_sdk import WebClient
from langchain_core.utils.uuid import uuid7
from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware
from langgraph.checkpoint.memory import InMemorySaver

# Agente em fase protótipo. Faz leitura de dados com sandbox E2B, gera relatório completo com gráficos e retorna para slack

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
#os.environ["E2B_API_KEY"] = getpass.getpass()
SCRIPT_DIR = Path(__file__).resolve().parent
PERSIST_DIRECTORY = (SCRIPT_DIR.parent / "data").as_posix()



def main():

    e2b_sandbox = Sandbox.create()
    backend = E2BSandbox(sandbox=e2b_sandbox)


    # Create sample sales data
    test = [
        ["Date", "Product", "Units Sold", "Revenue"],
        ["2025-08-01", "Widget A", 10, 250],
        ["2025-08-02", "Widget B", 5, 125],
        ["2025-08-03", "Widget A", 7, 175],
        ["2025-08-04", "Widget C", 3, 90],
        ["2025-08-05", "Widget B", 8, 200],
    ]

    def persist_data(): 
        # Convert to CSV bytes
        text_buf = io.StringIO()
        writer = csv.writer(text_buf)
        writer.writerows(test)
        csv_bytes = text_buf.getvalue().encode("utf-8")
        text_buf.close()

        # Upload to backend
        sandbox_file_path = "/home/user/vendas.csv"
        backend.upload_files([(sandbox_file_path, csv_bytes)])
        print(f"Arquivo enviado com sucesso para a Sandbox em: {sandbox_file_path}")



    ## ------------ SLACK CHANNEL ------------ ##

    slack_token = os.environ["SLACK_USER_TOKEN"]
    slack_client = WebClient(token=slack_token)
    channel = "C0BV1S30WQ5"

    @tool(parse_docstring=True)
    def slack_send_message(text: str, file_path: str | None = None) -> str:
        """Send message, optionally including attachments such as images.

        Args:
            text: (str) text content of the message
            file_path: (str) file path of attachment in the filesystem.
        """
        if not file_path:
            slack_client.chat_postMessage(channel=channel, text=text)
        else:
            fp = backend.download_files([file_path])
            slack_client.files_upload_v2(
                channel=channel,
                content=fp[0].content,
                initial_comment=text,
            )

        return "Message sent."


    ## ------------ MAIN AGENT ------------ ##

    checkpointer = InMemorySaver()

    agent = create_deep_agent(
        model="ollama:qwen2.5:3b", 
        tools=[slack_send_message],
        backend=backend,
        checkpointer=checkpointer,
    )

    thread_id = str(uuid7())
    config = {"configurable": {"thread_id": thread_id}}


    input_message = {
        "role": "user",
        "content": (
            "Analyze ./user/vendas.csv in the current dir and generate a beautiful plot. "
            "When finished, send your analysis and the plot to Slack using the tool."
        ),
    }
    stream = agent.stream_events(
        {"messages": [input_message]},
        config,
        version="v3",
    )
    for snapshot in stream.values:
        snapshot["messages"][-1].pretty_print()



if __name__ == "__main__":
    main()




