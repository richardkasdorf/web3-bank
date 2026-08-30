## 🤖 Arquitetura do Agente (Workflow)

O ecossistema do chatbot utiliza uma estrutura agêntica baseada em supervisão e RAG (Retrieval-Augmented Generation). Abaixo está o fluxo de tomada de decisão quando uma busca de documentos é invocada:

![Workflow do Agente](./docs/architecture/policy_subagent_workflow.png)

### Funcionamento do Fluxo:
1. O **Agent Executor** recebe a demanda do usuário e aciona o **Policy Supervisor Agent**.
2. O supervisor invoca a ferramenta de busca `search_documentation()`.
3. O desvio condicional valida se o banco vetorial **Chroma** retornou resultados:
   * **True:** Os dados são formatados com suas respectivas fontes e devolvidos para o Executor montar a resposta.
   * **False:** Uma condição de "Nenhum conteúdo encontrado" é retornada ao Supervisor para evitar loops e tratar o erro de forma amigável.
