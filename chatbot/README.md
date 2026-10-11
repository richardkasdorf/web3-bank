# Financial Chatbot (Satoshi)

Financial support assistant integrated into the digital bank, responsible for answering customer questions about balance, transactions, and blockchain-related topics, utilizing a local large language model (Ollama) and synchronized data from NEON.

## Architecture Overview

```
Frontend (React/TSX)
   │  POST /api/chatbot-text
   │  Header: Authorization: Bearer <token>
   ▼
FastAPI (bank_api)
   │  1. get_current_user() validates the JWT and identifies the logged-in user
   │  2. ChatbotService builds the context (profile + support) filtered by user_id
   │  3. Sends prompt to Ollama
   ▼
Ollama (local) — qwen2.5:3b model
   │  Generates response based solely on what was sent in the prompt
   ▼
FastAPI returns { "response": "..." } to the frontend
```

Ollama **never** accesses the database directly. All sensitive data is fetched by the backend, filtered by the `user_id` extracted from the JWT token, and only then included in the prompt.

## Requirements

- Python 3.11+ (via `bank_api` container)
- [Ollama](https://ollama.com) installed and running locally
- `qwen2.5:3b` model downloaded (`ollama pull qwen2.5:3b`)
- Database (NEON/Postgres) with `users`, `accounts`, and `transactions_ledger` tables already synchronized

## Environment Variables

Add to the `.env` file at the root of the project:

```dotenv
OLLAMA_URL=http://<host>:11434/api/generate
```

The value of `<host>` depends on where Docker is running:

| Scenario | Suggested Value |
|---|---|
| Docker Desktop (Windows/Mac) | `host.docker.internal` |
| Native Docker inside WSL2 (without Docker Desktop) | Windows gateway IP as seen by WSL (`ip route show default` inside WSL) — this IP is dynamic and may change on every reboot |
| Ollama running in another container | service name in `docker-compose.yml` (e.g., `ollama`) |

> ⚠️ If the host IP changes after rebooting Windows/WSL2, update `OLLAMA_URL` using the command `OLLAMA_HOST="<host>:11434"`.

## Ollama Configuration (running)
