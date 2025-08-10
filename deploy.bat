@echo off
REM NL-to-SQL Deployment Script for Windows

echo 🚀 Starting NL-to-SQL Application Deployment...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

echo [INFO] Prerequisites check passed ✅

REM Setup Python virtual environment
echo [INFO] Setting up Python virtual environment...
if not exist ".venv" (
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt

REM Setup backend
echo [INFO] Setting up Node.js backend...
cd backend

REM Install backend dependencies
call npm install

REM Copy environment file if it doesn't exist
if not exist ".env" (
    copy .env.example .env
    echo [WARNING] Please update backend/.env file with your MongoDB connection and JWT secret
)

cd ..

REM Setup frontend
echo [INFO] Setting up React frontend...
cd frontend

REM Install frontend dependencies
call npm install

REM Copy environment file if it doesn't exist
if not exist ".env" (
    copy .env.example .env
)

cd ..

echo [INFO] ✅ Setup completed successfully!
echo.
echo 🚀 To start the application:
echo 1. Terminal 1: python fastapi_server.py
echo 2. Terminal 2: cd backend ^&^& npm run dev
echo 3. Terminal 3: cd frontend ^&^& npm run dev
echo.
echo 📱 Access points:
echo - Frontend: http://localhost:3000
echo - Backend API: http://localhost:5000/api
echo - FastAPI Docs: http://localhost:8000/docs
echo.
echo [WARNING] Don't forget to update your environment variables!
pause
