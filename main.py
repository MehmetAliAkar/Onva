"""
SaaS Product Agent Platform - Main Application
"""
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time

from api.routes import agent, products, analytics, agents
from api.routes import jira as jira_routes
from core.config import settings
from core.logging import setup_logging

# Setup logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting SaaS Product Agent Platform...")
    # Startup: Initialize connections, load models, etc.
    yield
    # Shutdown: Cleanup resources
    logger.info("Shutting down SaaS Product Agent Platform...")


app = FastAPI(
    title="SaaS Product Agent Platform",
    description="Akıllı ürün satış ve destek agent platformu",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request details
    logger.info(f"=== REQUEST START ===")
    logger.info(f"Method: {request.method}")
    logger.info(f"Path: {request.url.path}")
    logger.info(f"Origin: {request.headers.get('origin', 'None')}")
    logger.info(f"Content-Type: {request.headers.get('content-type', 'None')}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Log response
    logger.info(f"Status: {response.status_code}")
    logger.info(f"Time: {process_time:.3f}s")
    
    # Log success/failure
    if 200 <= response.status_code < 300:
        logger.info(f"✅ SUCCESS: {request.method} {request.url.path} -> {response.status_code}")
    else:
        logger.error(f"❌ FAILED: {request.method} {request.url.path} -> {response.status_code}")
    
    logger.info(f"=== REQUEST END ===\n")
    
    return response

# CORS Middleware
logger.info(f"Allowed CORS origins: {settings.allowed_origins_list}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent.router, prefix="/api/v1/agent", tags=["Agent"])
app.include_router(agents.router, prefix="/api/v1", tags=["Agents Management"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(jira_routes.router, prefix="/api/v1", tags=["Jira Integration"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SaaS Product Agent Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "compagent-api"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
