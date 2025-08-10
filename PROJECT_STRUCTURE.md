# Project Structure

```
NL-TO-SQL/
│
├── 📁 nl_to_sql_package/          # Python NL-to-SQL Core Package
│   ├── 📁 core/                   # Core parsing components
│   │   ├── __init__.py
│   │   ├── ast_node.py            # AST Node definitions
│   │   ├── lexer.py               # Tokenizer/Lexer
│   │   ├── grammar.py             # Grammar parser
│   │   └── parser.py              # Main parser class
│   │
│   ├── 📁 utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── sql_translator.py      # SQL generation
│   │   ├── error_correction.py    # Error handling
│   │   └── visualization.py       # AST visualization
│   │
│   ├── 📁 database/              # Database management
│   │   ├── __init__.py
│   │   └── stock_manager.py       # Stock database manager
│   │
│   ├── 📁 api/                   # API interfaces
│   │   ├── __init__.py
│   │   └── web_api.py             # Web API endpoints
│   │
│   └── __init__.py               # Package initialization
│
├── 📁 backend/                   # Node.js Express Backend
│   ├── 📁 models/                # MongoDB models
│   │   ├── User.js               # User model
│   │   └── Query.js              # Query model
│   │
│   ├── 📁 routes/                # API routes
│   │   ├── auth.js               # Authentication routes
│   │   ├── queries.js            # Query processing routes
│   │   ├── users.js              # User management routes
│   │   └── analytics.js          # Analytics routes
│   │
│   ├── 📁 middleware/            # Express middleware
│   │   └── auth.js               # JWT authentication
│   │
│   ├── server.js                 # Express server setup
│   ├── package.json              # Node.js dependencies
│   └── .env.example              # Environment template
│
├── 📁 frontend/                  # React Frontend Application
│   ├── 📁 src/                   # Source code
│   │   ├── 📁 components/        # Reusable components
│   │   │   ├── Layout.jsx        # Main layout
│   │   │   ├── Navbar.jsx        # Navigation bar
│   │   │   ├── LoadingSpinner.jsx # Loading component
│   │   │   └── ...               # Other components
│   │   │
│   │   ├── 📁 pages/             # Page components
│   │   │   ├── Dashboard.jsx     # Main dashboard
│   │   │   ├── QueryParser.jsx   # Query input interface
│   │   │   ├── History.jsx       # Query history
│   │   │   ├── Analytics.jsx     # Analytics dashboard
│   │   │   ├── Login.jsx         # Login page
│   │   │   ├── Register.jsx      # Registration page
│   │   │   └── Profile.jsx       # User profile
│   │   │
│   │   ├── 📁 contexts/          # React contexts
│   │   │   └── AuthContext.jsx   # Authentication context
│   │   │
│   │   ├── 📁 services/          # API services
│   │   │   └── api.js            # API client
│   │   │
│   │   ├── App.jsx               # Main App component
│   │   ├── main.jsx              # React entry point
│   │   └── index.css             # Global styles
│   │
│   ├── index.html                # HTML template
│   ├── package.json              # Frontend dependencies
│   ├── vite.config.js            # Vite configuration
│   └── tailwind.config.js        # TailwindCSS config
│
├── fastapi_server.py             # FastAPI ML Service
├── requirements.txt              # Python dependencies
├── example.py                    # Usage example
├── README.md                     # Project documentation
└── .gitignore                    # Git ignore rules
```

## Key Components

### 🐍 Python ML Service (FastAPI)
- **Core Package**: Modular NL-to-SQL parsing engine
- **FastAPI Server**: RESTful API for ML model
- **Database**: SQLite for product data
- **Visualization**: AST tree generation

### 🟢 Backend API (Node.js/Express)
- **Authentication**: JWT-based user auth
- **Database**: MongoDB for user data & query history
- **Analytics**: Query performance tracking
- **Middleware**: Security, rate limiting, CORS

### ⚛️ Frontend (React/Vite)
- **Modern React**: Hooks, Context, Router
- **Styling**: TailwindCSS utility classes
- **State Management**: React Query for server state
- **Build Tool**: Vite for fast development

### 🗄️ Database Architecture
- **MongoDB**: User accounts, query history, analytics
- **SQLite**: Product inventory (embedded in Python service)

## Data Flow

1. **User Input** → React Frontend
2. **Authentication** → Express Backend → MongoDB
3. **Query Processing** → Express → FastAPI → Python ML
4. **Results** → FastAPI → Express → React
5. **Storage** → MongoDB (history/analytics)

## Microservices Benefits

- **Scalability**: Each service can scale independently
- **Technology Diversity**: Best tool for each job
- **Maintainability**: Clear separation of concerns
- **Deployment**: Independent deployment cycles
- **Development**: Teams can work in parallel
