
# Sistema de Busca de Documentos

Este projeto é uma aplicação em Python para busca em arquivos PDF e DOCX utilizando embeddings gerados com o modelo **sentence-transformers/paraphrase-multilingual-mpnet-base-v2**. A interface de busca é desenvolvida com **Streamlit**.

## Estrutura do Projeto

- `main.py`: Arquivo principal para executar a aplicação.
- `requirements.txt`: Arquivo com as dependências do projeto.
- `documentos`: Pasta onde devem ser armazenados os documentos PDF e DOCX.

## Requisitos

- Python 3.11
- CUDA (opcional, para aceleração com GPU)

## Configuração do Ambiente

1. Clone o repositório:
   ```bash
   git clone https://github.com/comais-labs/busca_documentos.git
   cd busca_documentos
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie a pasta `documentos` no diretório raiz do projeto:
   ```bash
   mkdir documentos
   ```

## Como Executar

1. Execute o script principal:
   ```bash
   streamlit run main.py
   ```

2. Acesse a aplicação pelo navegador no endereço `http://localhost:8501`.

## Funcionalidades

- Upload e processamento de documentos PDF e DOCX.
- Geração e atualização de embeddings para busca.
- Busca baseada em similaridade de textos.
- Download dos documentos encontrados.

## Tecnologias Utilizadas

- **PyMuPDF**: Para extração de texto de arquivos PDF.
- **python-docx**: Para extração de texto de arquivos DOCX.
- **LangChain**: Para manipulação de embeddings e busca.
- **Streamlit**: Para interface do usuário.
- **FAISS**: Para armazenamento de embeddings e buscas rápidas.

## Notas

- O modelo de embeddings utilizado é `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`.
- A aplicação detecta automaticamente se uma GPU está disponível e utiliza CUDA para acelerar as operações.



## Contato

Para dúvidas ou sugestões, entre em contato com [COMAIS Labs](https://www.comais.uft.edu.br).
graph TB
    subgraph UI["User Interface Layer"]
        UI_MAIN["Streamlit Web Interface"]:::ui
        UPLOAD["Upload Component"]:::ui
        SEARCH["Search Interface"]:::ui
        DOWNLOAD["Document Download"]:::ui
    end

    subgraph PROC["Processing Layer"]
        DOC_PROC{"Document Processor"}:::processing
        PDF["PDF Processor<br/>(PyMuPDF)"]:::processing
        DOCX["DOCX Processor<br/>(python-docx)"]:::processing
        TEXT_EX["Text Extraction<br/>Pipeline"]:::processing
    end

    subgraph EMB["Embedding Layer"]
        TRANS["Sentence Transformer<br/>(multilingual-mpnet)"]:::ml
        CUDA["CUDA Acceleration"]:::tech
    end

    subgraph SEARCH["Search Layer"]
        FAISS[(FAISS Vector<br/>Store)]:::storage
        LANG["LangChain Search<br/>Pipeline"]:::processing
    end

    subgraph STORE["Storage Layer"]
        DOC_STORE[(Document<br/>Storage)]:::storage
        EMB_STORE[(Embedding<br/>Storage)]:::storage
    end

    %% Connections
    USER((User)) --> UI_MAIN
    UI_MAIN --> UPLOAD
    UI_MAIN --> SEARCH
    UI_MAIN --> DOWNLOAD

    UPLOAD --> DOC_PROC
    DOC_PROC --> PDF
    DOC_PROC --> DOCX
    PDF --> TEXT_EX
    DOCX --> TEXT_EX
    TEXT_EX --> TRANS
    CUDA -.-> TRANS
    TRANS --> FAISS
    TRANS --> EMB_STORE
    DOC_PROC --> DOC_STORE

    SEARCH --> TRANS
    FAISS --> LANG
    LANG --> UI_MAIN

    %% Click Events
    click UI_MAIN "https://github.com/comais-labs/busca_documentos/blob/main/main.py"
    click UPLOAD "https://github.com/comais-labs/busca_documentos/blob/main/main.py"
    click SEARCH "https://github.com/comais-labs/busca_documentos/blob/main/main.py"
    click DOWNLOAD "https://github.com/comais-labs/busca_documentos/blob/main/main.py"

    %% Styling
    classDef ui fill:#3498db,stroke:#2980b9,color:white
    classDef processing fill:#2ecc71,stroke:#27ae60,color:white
    classDef storage fill:#f1c40f,stroke:#f39c12,color:black
    classDef ml fill:#9b59b6,stroke:#8e44ad,color:white
    classDef tech fill:#95a5a6,stroke:#7f8c8d,color:white

    %% Legend
    subgraph Legend
        L_UI["UI Component"]:::ui
        L_PROC["Processing Component"]:::processing
        L_STORE["Storage Component"]:::storage
        L_ML["ML Component"]:::ml
        L_TECH["Technical Component"]:::tech
    end
