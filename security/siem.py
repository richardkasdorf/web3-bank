import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# Security Information and Event Management
OLLAMA_URL = os.getenv('OLLAMA_URL', "http://127.0.0.1:11434")

model = ChatOllama(model="qwen2.5:3b", 
        temperature=0, 
        num_ctx=8192, 
        base_url=OLLAMA_URL,
        timeout=120.0
    )


prompt_template = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an expert Cybersecurity SOC (Security Operations Center) Analyst. "
        "Analyze the provided log lines and identify any suspicious activities, "
        "such as brute-force attacks (multiple consecutive login failures), port scanning, or code injections. "
        "If you find anything suspicious, respond with: 1) The suspicious IP address, 2) Type of attack detected, "
        "3) Severity level (Low, Medium, High), and 4) A mitigation recommendation."
    )),
    ("user", "Analyze these logs:\n\n{logs_input}")
])



with open("server.log", "r") as file:
    logs_content = file.read()


chain = prompt_template | model
resposta = chain.invoke({"logs_input": logs_content})

print(resposta.content)
