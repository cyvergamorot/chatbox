@echo off
echo ============================================
echo   Music Mood Recommender - Startup
echo ============================================
echo.

REM Start Backend
echo Starting Backend on port 8000...
start "Backend" cmd /k "cd /d c:\Users\Eli\chatbot\backend && venv\Scripts\activate && python -m src.main"

REM Wait for backend
timeout /t 5 /nobreak >nul

REM Start Frontend
echo Starting Frontend on port 5173...
start "Frontend" cmd /k "cd /d c:\Users\Eli\chatbot\frontend && npm run dev"

echo.
echo ============================================
echo System Started!
echo.
echo Open this in your browser:
echo   http://localhost:5173
echo.
echo Backend: http://localhost:8000
echo.
echo Press any key to exit...
pause >nul
