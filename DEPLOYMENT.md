# PDF-RAG Application Deployment Guide

## Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- Docker & Docker Compose (optional, for containerized deployment)
- GROQ API Key (get it from https://console.groq.com/)

### 1. Local Setup (Without Docker)

```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start Qdrant with Docker
docker run -p 6333:6333 qdrant/qdrant:latest

# In another terminal, start the app
uvicorn main:app --host 127.0.0.1 --port 8000
```

Then visit: **http://localhost:8000**

---

## Docker Deployment (Recommended)

### Prerequisites
- Docker & Docker Compose installed

### Setup

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys to `.env`:**
   ```env
   GROQ_API_KEY=your_api_key_here
   QDRANT_URL=http://qdrant:6333
   ```

3. **Start services:**
   ```bash
   docker-compose up -d
   ```

4. **Access the app:**
   - Frontend: http://localhost:8000
   - Qdrant API: http://localhost:6333

5. **View logs:**
   ```bash
   docker-compose logs -f app
   ```

6. **Stop services:**
   ```bash
   docker-compose down
   ```

---

## Cloud Deployments

### Railway.app

1. Push code to GitHub
2. Sign in at https://railway.app
3. Create new project → Import from GitHub
4. Set environment variables:
   - `GROQ_API_KEY`
   - `QDRANT_URL` (use Qdrant Cloud or Railway PostgreSQL)
5. Deploy

### Render.com

1. Push code to GitHub
2. Sign in at https://render.com
3. Create Web Service → Connect GitHub repo
4. Environment: Python 3.11
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
7. Set environment variables
8. Deploy

### Heroku

```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set GROQ_API_KEY=your_key

# Deploy
git push heroku main
```

### Azure App Service

```bash
# Install Azure CLI
az login

# Create resource group
az group create -n mygroup -l eastus

# Create app service plan
az appservice plan create -n myplan -g mygroup --sku B1 --is-linux

# Deploy
az webapp up -n your-app-name -g mygroup --runtime "python:3.11"

# Set environment variables
az webapp config appsettings set -n your-app-name -g mygroup --settings GROQ_API_KEY=your_key
```

### AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 pdf-rag-app

# Create environment
eb create prod

# Set environment variables
eb setenv GROQ_API_KEY=your_key

# Deploy
eb deploy
```

---

## Using Qdrant Cloud (for Production)

For better reliability, use managed Qdrant instead of local storage:

1. Sign up at https://cloud.qdrant.io
2. Create a cluster
3. Get your API URL and key
4. Update `.env`:
   ```env
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your_api_key
   ```

---

## Production Optimizations

### 1. Use Gunicorn with Multiple Workers
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app
```

### 2. Enable HTTPS/SSL
- Use Nginx as reverse proxy with SSL certificates
- Or use managed SSL from cloud provider

### 3. Environment Variables
Always use `.env` file with sensitive data:
```bash
cp .env.example .env
# Edit .env with your keys
```

### 4. Health Checks
- Frontend: GET `/`
- Add `/health` endpoint for monitoring

### 5. Database Persistence
- Qdrant storage persists to volumes
- Regular backups recommended

---

## Troubleshooting

### "Connection refused" Error
**Problem:** `Error: [WinError 10061] No connection could be made`

**Solution:**
```bash
# Start Qdrant
docker run -p 6333:6333 qdrant/qdrant:latest

# Or verify it's running
curl http://localhost:6333/health
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Change port in docker-compose.yml or:
docker-compose up -p 8001:8000
```

### Model Download Issues
The embedding model downloads on first run. Ensure you have:
- Stable internet connection
- ~70MB free disk space
- Set HF_TOKEN for faster downloads (optional)

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| GROQ_API_KEY | ✅ Yes | - | API key from https://console.groq.com/ |
| QDRANT_URL | ❌ No | http://localhost:6333 | Qdrant server URL |
| QDRANT_API_KEY | ❌ No | - | API key if using secured Qdrant |
| OPENAI_API_KEY | ❌ No | - | Optional OpenAI fallback |
| DEBUG | ❌ No | False | Enable debug logging |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Frontend UI |
| POST | `/upload` | Upload PDF file |
| POST | `/query` | Query document |
| DELETE | `/clear` | Clear database |

---

## Performance Tips

1. **Batch uploads:** Process multiple PDFs sequentially
2. **Optimize chunk size:** Adjust in `data_loader.py`
3. **Use GPU:** Install `fastembed-gpu` for faster embeddings
4. **Cache embeddings:** For production, pre-compute embeddings

---

## Support

For issues, check:
- `.env` file configuration
- Qdrant connection status
- GROQ API key validity
- Network/firewall settings
