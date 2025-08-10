#!/bin/bash

# NL-to-SQL Deployment Script

echo "🚀 Starting NL-to-SQL Application Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python &> /dev/null; then
    print_error "Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

print_status "Prerequisites check passed ✅"

# Setup Python virtual environment
print_status "Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Setup backend
print_status "Setting up Node.js backend..."
cd backend

# Install backend dependencies
npm install

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_warning "Please update backend/.env file with your MongoDB connection and JWT secret"
fi

cd ..

# Setup frontend
print_status "Setting up React frontend..."
cd frontend

# Install frontend dependencies
npm install

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

cd ..

print_status "✅ Setup completed successfully!"
echo ""
echo "🚀 To start the application:"
echo "1. Terminal 1: python fastapi_server.py"
echo "2. Terminal 2: cd backend && npm run dev"
echo "3. Terminal 3: cd frontend && npm run dev"
echo ""
echo "📱 Access points:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:5000/api"
echo "- FastAPI Docs: http://localhost:8000/docs"
echo ""
print_warning "Don't forget to update your environment variables!"
