@echo off
REM Run Phase 2 with Docker Compose
REM Roman Urdu: Yeh batch file Docker se application chalati hai

echo ============================================================
echo 🐳 Phase 2 Todo App - Docker Compose Setup
echo ============================================================
echo.

REM Check if Docker is available
echo 📍 Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Docker command not found in PATH!
    echo.
    echo 💡 Try these steps:
    echo    1. Open Docker Desktop from Start Menu
    echo    2. Wait for Docker to start (whale icon in system tray)
    echo    3. Run this script again
    echo.
    echo 🌐 Opening Docker Desktop...
    start "docker-desktop:"
    timeout /t 3 /nobreak >nul
    exit /b 1
)

echo ✅ Docker found!
docker --version
echo.

REM Check if Docker is running
echo 📍 Checking if Docker is running...
docker ps >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Docker is not running!
    echo.
    echo 💡 Starting Docker Desktop...
    start "docker-desktop:"
    echo    Please wait for Docker to start (30-60 seconds)...
    echo    Then run this script again.
    echo.
    timeout /t 5 /nobreak >nul
    exit /b 1
)

echo ✅ Docker is running!
echo.

REM Show Docker info
echo 📊 Docker Info:
docker info --format "{{.ServerVersion}}" 2>nul | findstr /v "^$"
echo.

REM Build and run with Docker Compose
echo 📍 Building Docker image...
docker-compose build

if errorlevel 1 (
    echo ❌ Docker build failed!
    exit /b 1
)

echo ✅ Docker image built!
echo.

echo 🚀 Starting containers...
docker-compose up -d

if errorlevel 1 (
    echo ❌ Docker Compose failed!
    exit /b 1
)

echo ✅ Containers started!
echo.

echo 📊 Container Status:
docker-compose ps

echo.
echo ============================================================
echo ✅ Phase 2 Application Running in Docker!
echo ============================================================
echo.
echo 📍 URLs:
echo    🏠 Home: http://localhost:8000
echo    📚 API Docs: http://localhost:8000/docs
echo    🏥 Health: http://localhost:8000/health
echo.
echo 🐳 Docker Commands:
echo    View logs: docker-compose logs -f web
echo    Stop: docker-compose down
echo    Restart: docker-compose restart
echo.
echo 🌐 Opening browser...
timeout /t 5 /nobreak >nul
start http://localhost:8000/docs

echo ============================================================
