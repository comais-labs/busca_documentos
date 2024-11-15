import pymupdf
from docx import Document
from langchain.docstore.document import Document as Document_langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter    
from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st
import glob
import os
import torch
import pickle

torch_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_name = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'
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
    pdf_paths = glob.glob(directory + '/*.pdf') 
    docx_paths = glob.glob(directory + '/*.docx')
    return pdf_paths + docx_paths

def process_documents(directory):
    document_paths = get_document_path(directory)
    documents=[]
    for document_path in document_paths:
        if document_path.endswith('.pdf'):
            text = extract_text_from_pdf(document_path)
        elif document_path.endswith('.docx'):
            text = extract_text_from_docx(document_path)
        else:
            continue
        doc = Document_langchain(page_content= text, metadata={'source': document_path})
        documents.append(doc)
    return documents

def create_embedding(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs_list=[]
    for doc in documents:
        splits = text_splitter.split_text(doc.page_content)
        for split in splits:
            new_doc  = Document_langchain(page_content=split, metadata={'source':doc.metadata['source']})
            docs_list.append(new_doc)
    vectorstore  = FAISS.from_documents(docs_list, embeddings)
    return vectorstore
    
def search_documents(query, vectorstore, k=5):
    results = vectorstore.similarity_search(query, k=5)
    return results

def main():
    documents_directory = "documentos"
    vectorstore_path = "vectorstore.pkl"
    st.title("Sistema de busca de arquivos")
    st.write("Este sistema permite que você faça buscas em arquivos PDF e DOCX")
    st.button('Atualizar embedding...')
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
            for res in results:
                file_path = res.metadata['source']
                st.write(f"Aquivo : {os.path.basename(file_path)}")
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                st.download_button(
                    label="Download",
                    data=file_data,
                    file_name=os.path.basename(file_path),
                    mime='application/octet-stream'
                )
        else:
            st.write('Nenhum documento encontrado!')
if __name__ == '__main__':
    main()

            


    