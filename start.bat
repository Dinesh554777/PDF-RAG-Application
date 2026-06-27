@echo off
REM PDF-RAG Application Startup Script for Windows

echo ================================
echo PDF-RAG Application Startup
echo ================================
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)

echo Starting Qdrant...
docker run -d -p 6333:6333 --name qdrant-server qdrant/qdrant:latest

echo Waiting for Qdrant to be ready...
timeout /t 5 /nobreak

REM Check if Qdrant is running
for /l %%i in (1,1,30) do (
    curl http://localhost:6333/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo Qdrant is ready!
        goto :qdrant_ready
    )
    echo Attempt %%i/30 - Waiting for Qdrant...
    timeout /t 1 /nobreak
)

echo WARNING: Qdrant may not be ready yet, but continuing...

:qdrant_ready
echo.
echo Starting FastAPI Application...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Start the application
uvicorn main:app --host 127.0.0.1 --port 8000

REM Cleanup on exit
echo.
echo Stopping Qdrant...
docker stop qdrant-server
docker rm qdrant-server
echo Done!
