import pymupdf
from pathlib import Path
from docx import Document # pip install python-docx
from langchain.docstore.document import Document as Document_langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter    
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss
from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st
import glob
import os
import torch
import pickle

torch_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_name = 'ricardo-filho/bert-base-portuguese-cased-nli-assin-2'
#model_name = 'sentence-transformers/paraphrase-xlm-r-multilingual-v1'
embeddings = HuggingFaceEmbeddings(model_name=model_name)

def extract_text_from_pdf(pdf_path):
    text = ''
    pdf = pymupdf.open(pdf_path)
    for page in pdf:
        text += page.get_text()
    pdf.close()
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text
    return text 

def get_document_path(directory):
    directory = Path(directory).resolve()
    pdf_paths = list(directory.glob("*.pdf"))
    docx_paths = list(directory.glob("*.docx"))
    return pdf_paths + docx_paths

def process_documents(directory):
    document_paths = get_document_path(directory)
    documents=[]
    for document_path in document_paths:
        if document_path.suffix == '.pdf':
            text = extract_text_from_pdf(document_path)
        elif document_path.suffix == '.docx':
            text = extract_text_from_docx(document_path)
        else:
            continue
        doc = Document_langchain(page_content= text, metadata={'source': document_path})
        documents.append(doc)
    return documents

def create_embedding(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    docs_list=[]
    for doc in documents:
        splits = text_splitter.split_text(doc.page_content)
        for split in splits:
            new_doc  = Document_langchain(page_content=split, metadata={'source':doc.metadata['source']})
            docs_list.append(new_doc)
    
    vectorstore  = FAISS.from_documents(docs_list, embeddings)
    import faiss

    index = faiss.IndexFlatL2(len(embeddings.embed_query("Olá Mundo!")))

    vectorstore = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
        )
    vectorstore.add_documents(docs_list)
    return vectorstore
    
def search_documents(query, vectorstore, k=5):
    """
    Busca documentos que correspondem à consulta, com base em um limiar de similaridade.

    Args:
        query (str): A consulta de busca.
        vectorstore: O armazenamento de vetores FAISS.
        k (int): Número máximo de resultados a retornar.
        similarity_threshold (float): Limiar mínimo de similaridade (0.0 a 1.0).

    Returns:
        list: Resultados filtrados por similaridade.
    """
    # Realiza a busca no vectorstore
    results = vectorstore.similarity_search(query, k=k*2)
    
    # Agrupando documentos por 'source'
    results = remove_duplicate_sources(results)
    # Retorna apenas os documentos que atendem ao limiar
    return results[:k]

def remove_duplicate_sources(results):
    """Remove documentos com fontes duplicadas da lista de resultados."""
    unique_sources = set()
    unique_results = []
    for res in results:
        source = res.metadata['source']
        if source not in unique_sources:
            unique_sources.add(source)
            unique_results.append(res)
            
    return unique_results
def main():
    documents_directory = "documentos"
    vectorstore_path = "vectorstore.pkl"
    st.title("Sistema de busca de arquivos")
    st.write("Este sistema permite que você faça buscas em arquivos PDF e DOCX")
    if st.button('Atualizar embedding...'):
        with st.spinner('Processando...'):
            documents = process_documents(documents_directory)
            vectorstore = create_embedding(documents)
            with open(vectorstore_path, 'wb') as f:
                pickle.dump(vectorstore, f)
            st.success('Embedding atualizado com sucesso!')
    if os.path.exists(vectorstore_path):
        with st.spinner('Carregando embedding...'):
            with open(vectorstore_path, 'rb') as f:
                vectorstore = pickle.load(f)
    else:
        st.error('Embedding não encontrado!')
    query = st.text_input('Digite sua busca:')

    if query:
        with st.spinner('Buscando...'):
            results = search_documents(query, vectorstore)
        st.write('Documentos encontrados:') 
        if results:
            for i, res in enumerate(results):
                file_path = res.metadata['source']
                st.write(f"Aquivo : {os.path.basename(file_path)}")
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                st.download_button(
                    key= i,
                    label="Download",
                    data=file_data,
                    file_name=os.path.basename(file_path),
                    mime='application/octet-stream'
                )
        else:
            st.write('Nenhum documento encontrado!')
if __name__ == '__main__':
    main()

            


    