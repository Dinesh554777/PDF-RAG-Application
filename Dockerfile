FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi>=0.138.0 \
    fastembed>=0.8.0 \
    groq>=1.5.0 \
    inngest>=0.5.18 \
    llama-index-core>=0.14.22 \
    llama-index-embeddings-fastembed>=0.6.0 \
    llama-index-readers-file>=0.6.0 \
    openai>=2.43.0 \
    python-dotenv>=1.2.2 \
    python-multipart>=0.0.32 \
    qdrant-client>=1.18.0 \
    streamlit>=1.58.0 \
    uvicorn>=0.49.0 \
    gunicorn>=23.0.0

# Expose port
EXPOSE 8000

# Run with gunicorn for production
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "main:app"]
