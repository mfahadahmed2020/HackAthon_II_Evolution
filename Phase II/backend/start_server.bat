@echo off
REM Start Phase 2 Application
REM Roman Urdu: Yeh batch file server ko start karti hai

echo ============================================================
echo 🚀 Phase 2 Todo App - Starting Server...
echo ============================================================
echo.

REM Check Python 3.12
echo 📍 Checking Python version...
py -3.12 --version
if errorlevel 1 (
    echo ❌ Python 3.12 not found!
    exit /b 1
)
echo ✅ Python 3.12 found!
echo.

REM Install dependencies
echo 📦 Checking dependencies...
py -3.12 -m pip install -r requirements.txt --quiet --disable-pip-version-check
echo ✅ Dependencies OK!
echo.

REM Create database folder
echo 🗄️  Creating database folder...
if not exist database mkdir database
echo ✅ Database folder ready!
echo.

echo 🌐 Starting FastAPI server...
echo    URL: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo    Health: http://localhost:8000/health
echo.
echo ============================================================
echo ⚠️  Server starting... Press Ctrl+C to stop
echo ============================================================
echo.

py -3.12 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
