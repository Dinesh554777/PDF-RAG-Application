# PDF-RAG-Application

An intelligent PDF document assistant powered by LLMs (Groq/OpenAI) and vector embeddings (FastEmbed). Upload PDFs and ask questions about their content using RAG (Retrieval-Augmented Generation).

## Features

- 📄 **PDF Upload & Processing** - Extract and chunk PDFs automatically
- 🧠 **Semantic Search** - Find relevant content using embeddings
- 💬 **AI-Powered Q&A** - Get answers using Groq or OpenAI LLMs
- 🚀 **Fast Local Embeddings** - FastEmbed for CPU-efficient embeddings
- 🗄️ **Vector Database** - Qdrant for semantic similarity search
- 🎨 **Modern UI** - Clean, responsive web interface

## Quick Start

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- GROQ API Key (free at https://console.groq.com)

### Option 1: Docker (Recommended)

```bash
# Clone and navigate to project
cd PDF-RAG-Application

# Copy environment template
cp .env.example .env

# Add your GROQ API key to .env
# GROQ_API_KEY=your_key_here

# Start services
docker-compose up -d

# Access at http://localhost:8000
```

### Option 2: Local Development

```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start Qdrant (in another terminal)
docker run -p 6333:6333 qdrant/qdrant:latest

# Start the app
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Option 3: Automated Startup Script

**Windows:**
```bash
.\start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

## Usage

1. **Upload PDF** - Click "Select PDF" or drag & drop your file
2. **Wait for Processing** - Document gets embedded and indexed
3. **Ask Questions** - Type your question in the chat
4. **Get Answers** - AI responds with relevant information from your document

## Project Structure

```
.
├── main.py              # FastAPI application
├── data_loader.py       # PDF loading & chunking
├── vector_db.py         # Qdrant vector database
├── custom_types.py      # TypeScript definitions
├── index.html           # Frontend UI
├── pyproject.toml       # Project configuration
├── docker-compose.yml   # Docker services
├── Dockerfile           # Container image
└── DEPLOYMENT.md        # Detailed deployment guide
```

## Configuration

Create a `.env` file with:

```env
GROQ_API_KEY=your_api_key_here
QDRANT_URL=http://localhost:6333
OPENAI_API_KEY=optional_key
```

See `.env.example` for all available options.

## Deployment

For production deployment to Railway, Render, Heroku, AWS, or Azure, see [DEPLOYMENT.md](DEPLOYMENT.md).

**Quick deployment:**
```bash
docker build -t pdf-rag .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key pdf-rag
```

## API Endpoints

- `GET /` - Frontend UI
- `POST /upload` - Upload PDF file
- `POST /query` - Query document
- `DELETE /clear` - Clear database

## Tech Stack

- **Backend**: FastAPI, Python
- **Embeddings**: FastEmbed (BAAI/bge-small-en-v1.5)
- **LLM**: Groq (llama-3.1-8b-instant)
- **Vector DB**: Qdrant
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker

## Troubleshooting

**"Connection refused" error:**
```bash
# Verify Qdrant is running
curl http://localhost:6333/health
```

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

**Port already in use:**
```bash
docker-compose up -p 8001:8000
```

## License

MIT

## Support

For issues and questions, refer to [DEPLOYMENT.md](DEPLOYMENT.md)
