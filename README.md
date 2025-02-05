
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

 
