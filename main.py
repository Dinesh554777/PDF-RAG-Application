import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import inngest
import inngest.fast_api
from dotenv import load_dotenv
import uuid
import os
from data_loader import load_and_chunk_pdf, embed_texts
from vector_db import QdrantStorage
from groq import Groq

load_dotenv()

inngest_client = inngest.Inngest(
    app_id="rag_app",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer()
)

groq_client = Groq()

@inngest_client.create_function(
    fn_id="RAG: Ingest PDF",
    trigger=inngest.TriggerEvent(event="rag/ingest_pdf")
)
async def rag_ingest_pdf(ctx: inngest.Context):
    file_path = ctx.event.data.get("file_path")
    
    # 1. Load and chunk PDF
    chunks = await ctx.step.run("load_and_chunk", lambda: load_and_chunk_pdf(file_path))
    
    if not chunks:
        return {"error": "No text extracted from PDF"}
        
    # 2. Generate Embeddings (using OpenAI via data_loader)
    embeddings = await ctx.step.run("embed_chunks", lambda: embed_texts(chunks))
    
    # 3. Upsert to Qdrant Database
    def upsert_to_qdrant():
        db = QdrantStorage()
        ids = [str(uuid.uuid4()) for _ in chunks]
        payloads = [{"text": chunk, "source": file_path} for chunk in chunks]
        db.upsert(ids, embeddings, payloads)
        return len(chunks)
        
    ingested = await ctx.step.run("upsert", upsert_to_qdrant)
    
    # Optional cleanup of temp file
    # os.remove(file_path)
    
    return {"ingested": ingested}


app = FastAPI()

# Mount Inngest API
inngest.fast_api.serve(app, inngest_client, functions=[rag_ingest_pdf])

# Serve Frontend
@app.get("/")
async def get_index():
    if not os.path.exists("index.html"):
        raise HTTPException(status_code=404, detail="Frontend file not found.")
    return FileResponse("index.html")

# API Routes
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Save file temporarily
    temp_path = f"temp_{uuid.uuid4()}.pdf"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
        
    # Trigger Inngest job to process asynchronously
    inngest_client.send(
        inngest.Event(
            name="rag/ingest_pdf",
            data={"file_path": temp_path}
        )
    )
    
    # Since Inngest runs async, we return immediately to the frontend
    return {"message": "File uploaded and processing started", "file_name": file.filename}

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_rag(request: QueryRequest):
    # 1. Embed user query
    query_vector = embed_texts([request.query])[0]
    
    # 2. Search Database for context
    db = QdrantStorage()
    search_res = db.search(query_vector, top_k=3)
    
    contexts = search_res["contexts"]
    
    if not contexts:
        return {"answer": "I don't have enough context to answer this question. Please upload a relevant PDF first.", "sources": [], "num_contexts": 0}
        
    # 3. Generate Answer with Groq
    context_text = "\n\n".join(contexts)
    prompt = f"Answer the user's question based ONLY on the following context. If the answer is not in the context, say 'I cannot answer this based on the provided document'.\n\nContext:\n{context_text}\n\nQuestion: {request.query}"
    
    completion = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    return {
        "answer": completion.choices[0].message.content,
        "sources": search_res["sources"],
        "num_contexts": len(contexts)
    }
