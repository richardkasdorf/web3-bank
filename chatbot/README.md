# 🤖 Intelligent Financial Agent with Generative AI

## Context

Virtual assistants in the financial sector are evolving from simple reactive chatbots to **intelligent and proactive agents**. In this challenge, you will conceptualize and prototype a financial agent that uses Generative AI to:

- **Anticipate needs** instead of just answering questions
- **Personalize** suggestions based on each customer's context
- **Co-create solutions** financial solutions in a consultative manner
- **Ensure security** and reliability in responses (anti-hallucination)

> [!TIP]
> In the [`examples/`](./examples/) folder, you will find implementation references for each step of this challenge.

---

## What You Must Deliver

### 1. Agent Documentation

Define **what** your agent does and **how** it works:

- **Use Case:** What financial problem does it solve? (e.g., investment consulting, goal planning, spending alerts)
- **Persona and Tone of Voice:** How does the agent behave and communicate?
- **Architecture:** Data flow and integration with the knowledge base
- **Security:** How to prevent hallucinations and ensure reliable answers?

📄 **Template:** [`docs/01-documentacao-agente.md`](./docs/01-documentacao-agente.md)

---

### 2. Knowledge Base

Use the **mock data** available in the [`data/`](./data/) folder to feed your agent:

| File | Format | Use in the Agent |
|---------|---------|---------------------|
| `history_chat.csv` | CSV | Contextualize previous interactions |
| `risk_profile.json` | JSON | Personalize recommendations by assessing the profile |
| `invest_options.json` | JSON | Suggest products suited to the profile |
| `transactions.csv` | CSV | Analyze the customer's spending patterns |

You can adapt or expand this data according to your use case.

📄 **Template:** [`docs/02-base-conhecimento.md`](./docs/02-base-conhecimento.md)

---

### 3. Agent Prompts

Document the prompts that define your agent's behavior:

- **System Prompt:** General instructions on behavior and restrictions
- **Interaction Examples:** Usage scenarios with expected input and output
- **Edge Cases Handling:** How the agent handles boundary situations

📄 **Template:** [`docs/03-prompts.md`](./docs/03-prompts.md)

---

### 4. Functional Application

Develop a **functional prototype** of your agent:

- Interactive chatbot (suggestion: Streamlit, Gradio, or similar)
- LLM integration (via API or local model)
- Connection to the knowledge base

📁 **Folder:** [`src/`](./src/)

---

### 5. Evaluation and Metrics

Describe how you evaluate the quality of your agent:

**Suggested Metrics:**
- Accuracy/assertiveness of responses
- Safe response rate (no hallucinations)
- Coherence with the customer's profile

📄 **Template:** [`docs/04-metricas.md`](./docs/04-metricas.md)

---

### 6. Pitch

Record a **3-minute pitch** (elevator style) presenting:

- What problem does your agent solve?
- How does it work in practice?
- Why is this solution innovative?

📄 **Template:** [`docs/05-pitch.md`](./docs/05-pitch.md)

---

## Suggested Tools

All the tools below have free versions:

| Category | Tools |
|-----------|-------------|
| **LLMs** | [ChatGPT](https://chat.openai.com/), [Copilot](https://copilot.microsoft.com/), [Gemini](https://gemini.google.com/), [Claude](https://claude.ai/), [Ollama](https://ollama.ai/) |
| **Development** | [Streamlit](https://streamlit.io/), [Gradio](https://www.gradio.app/), [Google Colab](https://colab.research.google.com/) |
| **Orchestration** | [LangChain](https://www.langchain.com/), [LangFlow](https://www.langflow.org/), [CrewAI](https://www.crewai.com/) |
| **Diagrams** | [Mermaid](https://mermaid.js.org/), [Draw.io](https://app.diagrams.net/), [Excalidraw](https://excalidraw.com/) |

---

## Repository Structure



```
📁 Estudos_Python/
│
├── 📁 docs/                          # Project documentation and datasets
│   ├── 📄 history_chat.csv           # Chat history database
│   ├── 📄 invest_options.json        # Investment products data
│   ├── 📄 knowledge.md               # Base of knowledge definition
│   ├── 📄 risk_profile.json          # Customer risk assessment profiles
│   └── 📄 transactions.csv           # Customer transaction records
│
├── 📄 models.py                      # Data models and structures
├── 📄 README.md                      # Main project documentation
├── 📄 route_chatbot.py               # Chatbot API routes and endpoints
├── 📄 services.py                    # Business logic and data loading
└── 📄 init.py                        # Python package initialization
```


---

## Final Tips

1. **Start with the prompt:** A good system prompt is the foundation of an effective agent
2. **Use the mock data:** They ensure consistency and avoid problems with sensitive data
3. **Focus on security:** In the financial sector, avoiding hallucinations is critical
4. **Test real scenarios:** Simulate questions that a real customer would ask
5. **Be direct in the pitch:** 3 minutes go by fast, get straight to the point