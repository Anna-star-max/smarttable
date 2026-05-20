@echo off
title SmartTable AI Service
color 0A

echo ========================================
echo     SmartTable AI Service - Starting
echo ========================================
echo.

cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+ first.
    pause
    exit /b 1
)

REM Check dependencies
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Dependencies not complete. Installing...
    call install.bat
)

REM Check .env
if not exist "backend\.env" (
    if not exist ".env" (
        echo [WARNING] .env file not found
        echo Please copy .env.example to .env and fill in your API Key
        echo.
        pause
        exit /b 1
    )
)

REM Get local IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr /v "Virtual"') do (
    set "LOCAL_IP=%%a"
    set "LOCAL_IP=!LOCAL_IP: =!"
)

echo.
echo ========================================
echo   Open browser and go to:
echo.
echo   Local: http://localhost:8000
if defined LOCAL_IP (
    echo   LAN: http://!LOCAL_IP!:8000
)
echo ========================================
echo.
echo Starting service...
echo.

start http://localhost:8000

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

pause