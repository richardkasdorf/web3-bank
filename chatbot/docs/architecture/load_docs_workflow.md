## Process Architecture (Workflow)

Structured script to load and read a .md file from a local folder where the directory will be pre-defined in the environment variable, split the document into *chunks*, and vectorize it with an embedding tool to optimize the AI model's context window.

![Script Workflow](./docs/architecture/load_docs_workflow.png)

### Note:
It must be done "manually", meaning the .py script must be executed in isolation.

### Script Steps:
1. The `load_local_docs()` function searches for and loads the file defined in the environment variable.
2. The *text_splitter* variable splits the file recursively and intelligently, then the *all_splits* variable executes the split definitively.
3. The *embeddings* variable translates the chunks into **mathematical language (vectors)**.
4. Next, *record_manager* records what has already been executed above, and the *vector store* variable stores it in the **Chroma** database.
