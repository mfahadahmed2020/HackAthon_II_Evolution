@echo off
REM Run Phase 2 Application
REM Roman Urdu: Yeh batch file application ko start karti hai

echo ============================================================
echo 🚀 Phase 2 Todo App - Starting Application...
echo ============================================================
echo.

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo ❌ requirements.txt not found!
    exit /b 1
)

echo 📦 Installing dependencies...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo ❌ Failed to install dependencies!
    exit /b 1
)

echo ✅ Dependencies installed!
echo.

echo 🗄️  Creating database folder...
if not exist database mkdir database

echo 🌐 Starting FastAPI server...
echo    URL: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo    Health: http://localhost:8000/health
echo.
echo ============================================================
echo ⚠️  Press Ctrl+C to stop the server
echo ============================================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
