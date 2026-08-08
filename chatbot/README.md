# Chatbot Financeiro (Satoshi)

Assistente de suporte financeiro integrado ao banco digital, responsável por responder perguntas dos clientes sobre saldo, transações e assuntos relacionados a blockchain, utilizando um modelo de linguagem local (Ollama) e dados sincronizados da NEON.

## Visão geral da arquitetura

```
Frontend (React/TSX)
   │  POST /api/chatbot-text
   │  Header: Authorization: Bearer <token>
   ▼
FastAPI (bank_api)
   │  1. get_current_user() valida o JWT e identifica o usuário logado
   │  2. ChatbotService monta o contexto (perfil + transações) filtrado por user_id
   │  3. Envia prompt para o Ollama
   ▼
Ollama (local) — modelo qwen2.5:3b
   │  Gera resposta com base apenas no que foi enviado no prompt
   ▼
FastAPI retorna { "response": "..." } para o frontend
```

O Ollama **nunca** acessa o banco de dados diretamente. Todo dado sensível é buscado pelo backend, filtrado pelo `user_id` extraído do token JWT, e só então incluído no prompt.

## Requisitos

- Python 3.11+ (via `bank_api` container)
- [Ollama](https://ollama.com) instalado e rodando localmente
- Modelo `qwen2.5:3b` baixado (`ollama pull qwen2.5:3b`)
- Banco de dados (NEON/Postgres) com as tabelas `users`, `accounts` e `transactions_ledger` já sincronizadas

## Variáveis de ambiente

Adicionar ao `.env` na raiz do projeto:

```dotenv
OLLAMA_URL=http://<host>:11434/api/generate
```

O valor de `<host>` depende de onde o Docker está rodando:

| Cenário | Valor sugerido |
|---|---|
| Docker Desktop (Windows/Mac) | `host.docker.internal` |
| Docker nativo dentro do WSL2 (sem Docker Desktop) | IP do gateway Windows visto pelo WSL (`ip route show default` dentro do WSL) — este IP é dinâmico e pode mudar a cada reinício |
| Ollama rodando em outro container | nome do serviço no `docker-compose.yml` (ex: `ollama`) |

> ⚠️ Se o IP do host mudar após reiniciar o Windows/WSL2, atualize `OLLAMA_URL` no `.env` e recrie o container (`docker compose up -d --build`).

## Configuração do Ollama (rodando local, fora do Docker)

O Ollama, por padrão, só aceita conexões vindas da própria máquina (`127.0.0.1`). Para que o container consiga acessá-lo, é necessário liberar conexões externas:

**1. Definir a variável `OLLAMA_HOST`** (permanente, via Variáveis de Ambiente do Sistema no Windows):
```
OLLAMA_HOST=0.0.0.0:11434
```

**2. Se o modelo estiver armazenado fora da pasta padrão** (ex: em outro disco/SSD), definir também:
```
OLLAMA_MODELS=<caminho para a pasta dos modelos>
```

**3. Liberar a porta no firewall do Windows** (PowerShell como Administrador):
```powershell
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow
```

**4. Confirmar que está escutando em todas as interfaces:**
```powershell
netstat -ano | findstr 11434
```
Deve aparecer `0.0.0.0:11434`, não `127.0.0.1:11434`.

**5. Subir o servidor:**
```powershell
ollama serve
```

## Estrutura de arquivos

```
chatbot/
├── data/
│   └── prompt.md          # System prompt do assistente (Satoshi)
├── models.py               # ChatRequest (schema da requisição)
├── services.py              # ChatbotService — lógica principal
└── router.py                 # Rota /api/chatbot-text
```

## Endpoint

### `POST /api/chatbot-text`

**Autenticação:** obrigatória (Bearer token / JWT)

**Request body:**
```json
{
  "message": "Quanto eu enviei essa semana?"
}
```

**Response (200):**
```json
{
  "response": "Você enviou 1.55 USDC no dia 27/07/2026."
}
```

**Possíveis erros:**
| Status | Causa |
|---|---|
| 400 | Mensagem vazia |
| 401 | Token ausente, inválido ou expirado |
| 500 | Erro interno (banco de dados ou processamento) |
| 503 | Ollama indisponível |

## Como o contexto do usuário é montado

O `ChatbotService.generate_reply(user_id, message)`:

1. Verifica se a mensagem contém palavras-chave financeiras (`saldo`, `balance`, `transaction`, `sent`, `recebi`, etc.)
2. Se sim, busca na NEON:
   - Perfil do usuário (`_get_user_profile`)
   - Últimas transações, considerando o usuário como remetente **ou** destinatário (`_get_user_transactions`)
3. Monta o prompt final combinando o `system_prompt` (de `data/prompt.md`) + contexto do cliente + a pergunta
4. Envia ao Ollama via `POST /api/generate`

Isso evita enviar dados financeiros desnecessários em mensagens simples (ex: "Olá!"), reduzindo o tamanho do prompt e o tempo de resposta.

## Segurança

- O `user_id` usado para consultar dados **nunca** vem do corpo da requisição — é sempre extraído do JWT validado por `get_current_user()`, evitando que um usuário consulte dados de outra conta.
- Valores monetários (`Decimal`) são convertidos para `float` apenas na hora de montar o contexto textual enviado ao modelo — o valor original em `Decimal` é preservado no restante do sistema para evitar erros de arredondamento em operações financeiras.
- Sessões de banco de dados abertas fora do ciclo de vida do FastAPI (`Depends`) usam uma função dedicada (`get_db_session`), sempre fechadas em bloco `finally`.

## Troubleshooting

| Sintoma | Causa provável | Solução |
|---|---|---|
| `Connection refused` para `localhost:11434` | Ollama rodando dentro de outro contexto de rede (container vs host) | Ajustar `OLLAMA_URL` conforme a tabela acima |
| `{"models":[]}` ao consultar `/api/tags` | `OLLAMA_MODELS` apontando para pasta errada | Definir `OLLAMA_MODELS` com o caminho correto e reiniciar o Ollama |
| Resposta demorando 30s+ e retornando 500 | Timeout do `requests.post` menor que o tempo real de geração | Aumentar `timeout` na chamada e/ou reduzir tamanho do prompt |
| Chatbot menciona dados de mercado inexistentes (TVL, CPI, etc.) | Instrução antiga no `prompt.md` forçando esses campos | Revisar `prompt.md` — não instruir o modelo a sempre incluir métricas que não estão no contexto |
| Chatbot traz extrato mesmo em mensagens como "Olá!" | Contexto financeiro sendo enviado em toda mensagem, sem filtro | Confirmar que o filtro por palavra-chave (`needs_context`) está ativo em `generate_reply` |
| `401 Unauthorized` ao chamar o endpoint | Token não enviado no header `Authorization` pelo frontend | Confirmar que o `fetch` inclui `Authorization: Bearer <token>` |

## Notas

- Este chatbot é um projeto de estudo. O modelo `qwen2.5:3b` é pequeno e pode ter dificuldade em seguir instruções complexas de forma consistente — para maior confiabilidade, considere um modelo maior se o hardware permitir.
- Nenhuma recomendação de investimento deve ser tratada como aconselhamento financeiro real.