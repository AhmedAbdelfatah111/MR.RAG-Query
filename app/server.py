
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from langserve import add_routes
from app.chains import get_rag_chain, get_summary_chain
from app.ingestion import ingest_file
import shutil
import os

app = FastAPI(
    title="Smart Contract Assistant",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

os.makedirs("data/uploads", exist_ok=True)

class QuestionInput(BaseModel):
    input: str

@app.post("/rag/invoke")
async def rag_invoke(body: QuestionInput):
    try:
        chain = get_rag_chain()
        result = chain.invoke(body.input)
        return {"output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

add_routes(
    app,
    get_summary_chain(),
    path="/summary",
)

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    file_path = f"data/uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        num_chunks = ingest_file(file_path)
        return {"message": f"Successfully ingested {file.filename}", "chunks": num_chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

