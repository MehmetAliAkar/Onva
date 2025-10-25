"""
SaaS Product Agent Platform - Main Application
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.routes import agent, products, analytics
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

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent.router, prefix="/api/v1/agent", tags=["Agent"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])


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
