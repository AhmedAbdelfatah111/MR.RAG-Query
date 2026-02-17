import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

VECTOR_STORE_PATH = "data/faiss_index"

def get_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.exists(VECTOR_STORE_PATH):
        try:
            vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
            return vector_store
        except:
            pass
    
    return None

def save_vector_store(vector_store):
    vector_store.save_local(VECTOR_STORE_PATH)



