## Arquitetura do processo (Workflow)

Script estruturado para carregar e ler um arquivo .md de uma pasta local onde o diretório será pré-definido na variável de ambiente, dividir o documento em *chunks* e vetorizar com a ferramenta embedding a fim de otimizar a janela de contexto do modelo de IA.

![Workflow do Script](./docs/architecture/load_docs_workflow.png)

### Observação:
Deve ser feito de maneira "manual", ou seja, o script .py deve ser executado isoladamente. 

### Etapas do script:
1. A função `load_local_docs()` busca e carrega o arquivo definido na variável de ambiente.
2. A variável *text_splitter* divide o arquivo de forma recursiva e inteligente, em seguida a variável *all_splits* executa o split de forma definitiva.
3. A variável *embeddings* traduz os chunks para a **linguagem matemática (vetores)**.
4. Na sequência *record_manager* faz um registro do que já foi executado acima e a variável *vector store* armazena no banco de dados **Chroma**.

