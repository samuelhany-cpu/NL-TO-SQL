# NL-to-SQL Full Stack Application

A complete full-stack application that converts natural language queries to SQL using Python, FastAPI, Node.js, React, and MongoDB.

![Project Banner](https://img.shields.io/badge/NL--to--SQL-Full%20Stack-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=flat-square)
![Node.js](https://img.shields.io/badge/Node.js-18+-green?style=flat-square)
![React](https://img.shields.io/badge/React-18-blue?style=flat-square)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?style=flat-square)

## 🌟 Features

- 🧠 **Smart NL-to-SQL Parsing**: Convert natural language to SQL queries
- 🔐 **User Authentication**: Secure JWT-based authentication
- 📊 **Analytics Dashboard**: Query performance and usage analytics
- 🎨 **Modern UI**: Responsive React interface with TailwindCSS
- 🔍 **Query History**: Track and manage previous queries
- 🖼️ **AST Visualization**: Visual representation of query parsing
- 🔄 **Real-time Processing**: Fast query parsing and execution
- 📱 **Mobile Responsive**: Works seamlessly on all devices

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │────│   Express API   │────│    MongoDB      │
│  (Port 3000)    │    │   (Port 5000)   │    │     Atlas       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                │
                       ┌─────────────────┐
                       │   FastAPI NL    │
                       │   to SQL Parser │
                       │   (Port 8000)   │
                       └─────────────────┘
```

## Tech Stack

### Frontend
- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **React Query** - Server state management
- **Axios** - HTTP client
- **React Hook Form** - Form handling
- **Recharts** - Data visualization

### Backend (API Server)
- **Node.js** - JavaScript runtime
- **Express.js** - Web framework
- **MongoDB** - NoSQL database
- **Mongoose** - MongoDB ODM
- **JWT** - Authentication
- **Bcrypt** - Password hashing
- **Helmet** - Security middleware

### ML Service (NL-to-SQL Parser)
- **FastAPI** - Modern Python web framework
- **Python 3.8+** - Programming language
- **PLY** - Python Lex-Yacc parser
- **SQLite** - Sample database
- **Matplotlib** - Visualization
- **NetworkX** - Graph visualization

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+ and pip
- MongoDB (local or cloud)
- Git

## Installation & Setup

### 1. Clone and Setup Project

```bash
# Clone the repository
git clone <your-repo-url>
cd NL-TO-SQL

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Setup MongoDB

#### Option A: Local MongoDB
1. Install MongoDB Community Edition
2. Start MongoDB service
3. Create database: `nl_to_sql_db`

#### Option B: MongoDB Atlas (Cloud)
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create cluster and get connection string
3. Update connection string in backend/.env

### 3. Setup Backend (Express API)

```bash
cd backend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env file with your settings
# Update MONGODB_URI, JWT_SECRET, etc.

# Start development server
npm run dev
```

### 4. Setup Frontend (React)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 5. Setup FastAPI ML Service

```bash
# From root directory, ensure virtual environment is activated
cd ./

# Start FastAPI server
python fastapi_server.py
```

## Environment Variables

### Backend (.env)
```env
NODE_ENV=development
PORT=5000
MONGODB_URI=mongodb://localhost:27017/nl_to_sql_db
JWT_SECRET=your-super-secret-jwt-key-here
FASTAPI_URL=http://localhost:8000
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
CORS_ORIGIN=http://localhost:3000
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000/api
```

## Running the Application

### Development Mode

1. **Start MongoDB** (if running locally)

2. **Start FastAPI ML Service** (Terminal 1):
```bash
# Activate Python virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Start FastAPI server
python fastapi_server.py
```

3. **Start Express Backend** (Terminal 2):
```bash
cd backend
npm run dev
```

4. **Start React Frontend** (Terminal 3):
```bash
cd frontend
npm run dev
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **FastAPI Docs**: http://localhost:8000/docs
- **FastAPI Service**: http://localhost:8000

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout user

### Query Endpoints
- `POST /api/queries/parse` - Parse natural language query
- `GET /api/queries/history` - Get user query history
- `GET /api/queries/:id` - Get specific query
- `POST /api/queries/:id/feedback` - Add feedback
- `DELETE /api/queries/:id` - Delete query

### Analytics Endpoints
- `GET /api/analytics/dashboard` - User analytics
- `GET /api/analytics/system` - System analytics (admin)

### FastAPI Endpoints
- `POST /parse` - Parse natural language to SQL
- `GET /products` - Get all products
- `GET /products/categories` - Get categories
- `POST /products/search` - Search products

## Features

### Core Features
- ✅ Natural language to SQL conversion
- ✅ User authentication and authorization
- ✅ Query history and management
- ✅ Real-time query parsing
- ✅ AST visualization
- ✅ Multiple query support
- ✅ Error correction and suggestions

### Dashboard Features
- ✅ User analytics and insights
- ✅ Query success rates
- ✅ Performance metrics
- ✅ Category-wise analysis
- ✅ Visual charts and graphs

### Advanced Features
- ✅ Compound query support
- ✅ Query complexity analysis
- ✅ Feedback system
- ✅ Search and filtering
- ✅ Export capabilities
- ✅ Theme support (light/dark)

## Sample Queries

Try these natural language queries:

1. **Simple Inventory**:
   - "How many mobiles do we have?"
   - "Show me all TVs in stock"
   - "What computers are available?"

2. **Compound Queries**:
   - "How many mobiles we have ? How many TVs we have ?"
   - "Show computers ? List all tablets ?"

3. **Specific Products**:
   - "How many units of item TV-1234 in the store"
   - "Show me mobile MOB-001"

## Deployment

### Production Build

#### Frontend
```bash
cd frontend
npm run build
# Serve dist/ folder with nginx or static hosting
```

#### Backend
```bash
cd backend
npm start
# Use PM2 for process management in production
```

#### FastAPI
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker fastapi_server:app
```

### Docker Deployment

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  fastapi:
    build: .
    command: uvicorn fastapi_server:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    depends_on:
      - mongodb

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    depends_on:
      - mongodb
      - fastapi
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/nl_to_sql_db
      - FASTAPI_URL=http://fastapi:8000

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  mongo_data:
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Check MongoDB service is running
   - Verify connection string in .env
   - Check network connectivity

2. **FastAPI Service Unavailable**
   - Ensure Python virtual environment is activated
   - Check if port 8000 is available
   - Verify Python dependencies are installed

3. **Frontend Build Errors**
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility
   - Verify environment variables

4. **CORS Issues**
   - Check CORS_ORIGIN in backend .env
   - Verify API URL in frontend .env
   - Ensure ports match configuration

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email samuelhany500@gmail.com or create an issue in the repository.

## 👨‍💻 Author

**Samuel Ehab Kamal**
- GitHub: [@samuelhany-cpu](https://github.com/samuelhany-cpu)
- Email: samuelhany500@gmail.com

## 🙏 Acknowledgments

- PLY (Python Lex-Yacc) for parsing capabilities
- FastAPI for the modern Python web framework
- React and TailwindCSS for the beautiful UI
- MongoDB Atlas for cloud database hosting
