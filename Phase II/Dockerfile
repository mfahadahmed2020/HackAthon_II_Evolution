# Phase 2 Todo App - Dockerfile
# Roman Urdu: Yeh Dockerfile FastAPI application ko containerize karta hai

# Python 3.11 slim image use kar rahe hain - chhota aur fast
FROM python:3.11-slim

# Metadata - application ki jaankari
LABEL maintainer="HackAthon Phase 2"
LABEL description="Todo App with Docker, Categories, Recurring Tasks, Real-time Updates"
LABEL version="2.0.0"

# Security: Non-root user create kar rahe hain
# Roman Urdu: Security ke liye appuser naam ka user bana rahe hain
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Working directory set karna
WORKDIR /app

# Environment variables - production settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Requirements file copy karna - layer caching ke liye pehle
# Roman Urdu: Pehle requirements.txt copy karte hain taaki Docker cache use kar sake
COPY requirements.txt .

# Dependencies install karna
# Roman Urdu: Saare Python packages install kar rahe hain
RUN pip install --no-cache-dir -r requirements.txt

# Application code copy karna
# Roman Urdu: Ab pura application code copy karte hain
COPY . .

# Database folder create karna (SQLite ke liye)
# Roman Urdu: SQLite database ke liye folder bana rahe hain
RUN mkdir -p /app/database && \
    mkdir -p /app/logs && \
    chown -R appuser:appgroup /app

# Permissions set karna - security ke liye
# Roman Urdu: appuser ko ownership de rahe hain
RUN chown -R appuser:appgroup /app

# Non-root user par switch karna
# Roman Urdu: Security ke liye ab non-root user par aa rahe hain
USER appuser

# Port expose karna - FastAPI default port 8000
# Roman Urdu: Application port 8000 par chalega
EXPOSE 8000

# Health check - application healthy hai ya nahi
# Roman Urdu: Har 30 seconds mein health check kar rahe hain
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Application start karne ka command
# Roman Urdu: Uvicorn server ko start kar rahe hain
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
