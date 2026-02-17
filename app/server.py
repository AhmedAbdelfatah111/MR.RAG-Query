from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langserve import add_routes
from app.chains import get_rag_chain, get_summary_chain
from app.ingestion import ingest_file
from sse_starlette.sse import EventSourceResponse
import shutil
import os
import json

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

@app.post("/rag/stream")
async def rag_stream(body: QuestionInput):
    async def event_generator():
        try:
            chain = get_rag_chain()
            async for chunk in chain.astream(body.input):
                yield {"event": "data", "data": json.dumps(chunk)}
            yield {"event": "end", "data": ""}
        except Exception as e:
            yield {"event": "error", "data": json.dumps({"error": str(e)})}

    return EventSourceResponse(event_generator())


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


