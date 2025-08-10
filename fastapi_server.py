from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import base64
import io
import os
import logging
from nl_to_sql_package import NLToSQLParser
from nl_to_sql_package.database.stock_manager import StockManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NL to SQL API",
    description="Natural Language to SQL Query Parser API by Samuel Ehab Kamal",
    version="1.0.0",
    contact={
        "name": "Samuel Ehab Kamal",
        "email": "samuelhany500@gmail.com",
        "url": "https://github.com/samuelhany-cpu"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the parser and stock manager
parser = NLToSQLParser()
stock_manager = StockManager()

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    include_visualization: bool = False

class QueryResponse(BaseModel):
    success: bool
    original_query: str
    corrected_query: Optional[str] = None
    sql_queries: List[str]
    results: List[Dict[str, Any]]
    visualization: Optional[str] = None  # Base64 encoded PNG
    debug_info: Optional[Dict[str, Any]] = None

class ProductResponse(BaseModel):
    products: List[Dict[str, Any]]
    total_count: int

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str

@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        service="NL to SQL Parser",
        version="1.0.0"
    )

@app.post("/parse", response_model=QueryResponse)
async def parse_query(request: QueryRequest):
    """
    Parse natural language query and return SQL with results
    """
    try:
        # Parse the query
        result = parser.parse(request.query)
        
        if not result['success']:
            raise HTTPException(
                status_code=400, 
                detail=f"Parse error: {result.get('error', 'Unknown error')}"
            )
        
        # Execute queries and get results
        sql_results = []
        for sql_query in result['sql_queries']:
            try:
                db_result = stock_manager.execute_query(sql_query)
                sql_results.append({
                    'sql': sql_query,
                    'data': db_result,
                    'count': len(db_result) if db_result else 0
                })
            except Exception as e:
                sql_results.append({
                    'sql': sql_query,
                    'error': str(e),
                    'data': [],
                    'count': 0
                })
        
        # Generate visualization if requested
        visualization_b64 = None
        if request.include_visualization and result.get('ast'):
            try:
                # Create visualization
                if isinstance(result['ast'], list):
                    # Multiple queries
                    from nl_to_sql_package.core.ast_node import ASTNode
                    png_path = ASTNode.create_compound_png(result['ast'])
                else:
                    # Single query
                    png_path = result['ast'].create_png()
                
                # Convert to base64
                if png_path and os.path.exists(png_path):
                    with open(png_path, 'rb') as img_file:
                        visualization_b64 = base64.b64encode(img_file.read()).decode('utf-8')
                    # Clean up temp file
                    os.remove(png_path)
            except Exception as e:
                print(f"Visualization error: {e}")
        
        return QueryResponse(
            success=True,
            original_query=request.query,
            corrected_query=result.get('corrected_query'),
            sql_queries=result['sql_queries'],
            results=sql_results,
            visualization=visualization_b64,
            debug_info=result.get('debug_info') if request.include_visualization else None
        )
        
    except Exception as e:
        logger.error(f"Query parsing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products", response_model=ProductResponse)
async def get_products():
    """
    Get all products in the database
    """
    try:
        products = stock_manager.get_all_products()
        return ProductResponse(
            products=products,
            total_count=len(products)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/categories")
async def get_categories():
    """
    Get all product categories
    """
    try:
        categories = stock_manager.get_categories()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/products/search")
async def search_products(query: str):
    """
    Search products by name or ID
    """
    try:
        results = stock_manager.search_products(query)
        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting NL-to-SQL FastAPI server...")
    logger.info("📚 API Documentation available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
