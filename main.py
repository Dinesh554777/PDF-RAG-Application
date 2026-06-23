import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import uuid
import os
from data_loader import load_and_chunk_pdf, embed_texts
from vector_db import QdrantStorage
from groq import Groq

load_dotenv()

groq_client = Groq()
app = FastAPI()

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
        
    try:
        # 1. Load and chunk PDF
        chunks = load_and_chunk_pdf(temp_path)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No text extracted from PDF")
            
        # 2. Generate Embeddings (using FastEmbed locally)
        embeddings = embed_texts(chunks)
        # FastEmbed returns a generator, convert to list so we can pass to Qdrant
        embeddings_list = list(embeddings)
        
        # 3. Upsert to Qdrant Database
        db = QdrantStorage()
        ids = [str(uuid.uuid4()) for _ in chunks]
        payloads = [{"text": chunk, "source": file.filename} for chunk in chunks]
        db.upsert(ids, embeddings_list, payloads)
        
        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return {"message": "File successfully embedded and ready for questions!", "file_name": file.filename, "chunks_processed": len(chunks)}
        
    except Exception as e:
        # Cleanup on failure
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_rag(request: QueryRequest):
    # 1. Embed user query
    embeddings = list(embed_texts([request.query]))
    query_vector = embeddings[0]
    
    # 2. Search Database for context
    db = QdrantStorage()
    search_res = db.search(query_vector, top_k=3)
    
    contexts = search_res["contexts"]
    
    if not contexts:
        return {"answer": "I don't have enough context to answer this question. Please upload a relevant PDF first.", "sources": [], "num_contexts": 0}
        
    # 3. Generate Answer with Groq
    context_text = "\n\n".join(contexts)
    prompt = f"You are a helpful assistant analyzing a document. Answer the user's question based on the following context. You can interpret the data, summarize, or do math if needed. If the data is completely unrelated, say 'I cannot answer this based on the provided document'.\n\nContext:\n{context_text}\n\nQuestion: {request.query}"
    
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    return {
        "answer": completion.choices[0].message.content,
        "sources": search_res["sources"],
        "num_contexts": len(contexts)
    }
