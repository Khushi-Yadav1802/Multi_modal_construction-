@echo off
title Construction Intelligence Platform
color 0B
echo.
echo  ============================================================
echo    Multimodal Construction Intelligence Platform
echo    Skill Wallet Capstone Project 1
echo  ============================================================
echo.

:: Step 1 - Install dependencies
echo  [1/2] Installing Python dependencies...
pip install fastapi uvicorn[standard] python-multipart google-generativeai Pillow requests python-dotenv --quiet
if errorlevel 1 (
    echo  ERROR: pip install failed. Make sure Python is installed.
    pause
    exit /b 1
)
echo  [1/2] Dependencies ready!
echo.

:: Step 2 - Start backend server
echo  [2/2] Starting FastAPI backend on http://localhost:8000
echo.
echo  ============================================================
echo   OPEN YOUR BROWSER AT: http://localhost:8000
echo  ============================================================
echo.
echo  Press Ctrl+C to stop the server.
echo.

cd /d "%~dp0backend"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
