@echo off
echo Starting ATS Resume Optimization System...
echo.
echo Starting Backend Server (Port 8000)...
cd /d "%~dp0backend"
start "ATS Backend" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul

echo.
echo Starting Frontend Server (Port 3000)...
cd /d "%~dp0frontend"
start "ATS Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo ATS System is starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press any key to open the application in your browser...
pause >nul
start http://localhost:3000
