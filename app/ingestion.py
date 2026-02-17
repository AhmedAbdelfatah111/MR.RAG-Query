
import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.vector_store import get_vector_store, save_vector_store, VECTOR_STORE_PATH

def ingest_file(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == ".pdf":
        loader = PyPDFLoader(file_path)
    elif file_extension == ".docx":
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    
    splits = text_splitter.split_documents(documents)
    
    vector_store = get_vector_store()
    
    if vector_store is None:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = FAISS.from_documents(documents=splits, embedding=embeddings)
    else:
        vector_store.add_documents(documents=splits)
    
    save_vector_store(vector_store)
    
    return len(splits)
