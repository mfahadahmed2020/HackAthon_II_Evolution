@echo off
echo ============================================================
echo Starting JWT Authentication and Tasks API
echo ============================================================
echo.

REM Set environment variables
set DATABASE_URL=postgresql://neondb_owner:npg_Ceb1u7LlsctV@ep-holy-band-a73gc162-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require
set PYTHONPATH=E:\Python Codes\HackAthon 2\Phase II

echo Database: Neon PostgreSQL
echo Connection: ep-holy-band-a73gc162-pooler.ap-southeast-2.aws.neon.tech
echo CORS: http://localhost:3000
echo.
echo Starting server on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start server with Python 3.12
py -3.12 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
