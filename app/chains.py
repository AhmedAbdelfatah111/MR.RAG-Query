from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from app.vector_store import get_vector_store
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "stepfun/step-3.5-flash:free"

def get_llm():
    return ChatOpenAI(
        model=MODEL_NAME,
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        streaming=True,
    )

def get_rag_chain():
    vector_store = get_vector_store()
    
    if vector_store is None:
        model = get_llm()
        prompt = ChatPromptTemplate.from_template("No documents available. Please upload a document first.")
        return prompt | model | StrOutputParser()
        
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    
    template = """You are a helpful contract assistant. Answer the question thoroughly and accurately based on the following context from the uploaded document.

Context:
{context}

Question: {question}

Provide a detailed and complete answer. If the information is found in the context, include specific details such as numbers, dates, and exact terms."""
    prompt = ChatPromptTemplate.from_template(template)
    model = get_llm()
    
    def extract_question(input_val):
        if isinstance(input_val, dict):
            return input_val.get("question", input_val.get("input", str(input_val)))
        return str(input_val)
    
    chain = (
        RunnableLambda(extract_question)
        | {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain

def get_summary_chain():
    model = get_llm()
    prompt = ChatPromptTemplate.from_template("Summarize the following content:\n\n{context}")
    chain = prompt | model | StrOutputParser()
    return chain


