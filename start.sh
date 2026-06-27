#!/bin/bash
# PDF-RAG Application Startup Script for macOS/Linux

echo "================================"
echo "PDF-RAG Application Startup"
echo "================================"
echo ""

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "ERROR: Docker is not running"
    echo "Please start Docker and try again"
    exit 1
fi

echo "Starting Qdrant..."
docker run -d -p 6333:6333 --name qdrant-server qdrant/qdrant:latest

echo "Waiting for Qdrant to be ready..."
sleep 5

# Check if Qdrant is running
for i in {1..30}; do
    if curl -s http://localhost:6333/health > /dev/null 2>&1; then
        echo "Qdrant is ready!"
        break
    fi
    echo "Attempt $i/30 - Waiting for Qdrant..."
    sleep 1
done

echo ""
echo "Starting FastAPI Application..."
echo ""

# Activate virtual environment
source .venv/bin/activate

# Start the application
uvicorn main:app --host 127.0.0.1 --port 8000

# Cleanup on exit
echo ""
echo "Stopping Qdrant..."
docker stop qdrant-server
docker rm qdrant-server
echo "Done!"
