"""
Analytics API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime, timedelta

from core.logging import logger

router = APIRouter()


class ConversationMetrics(BaseModel):
    """Conversation metrics model"""
    total_conversations: int
    avg_conversation_length: float
    avg_response_time: float
    satisfaction_rate: float


class ProductMetrics(BaseModel):
    """Product metrics model"""
    product_id: str
    total_inquiries: int
    configuration_requests: int
    conversion_rate: float
    top_questions: List[str]


class AgentPerformance(BaseModel):
    """Agent performance model"""
    total_interactions: int
    successful_resolutions: int
    escalations: int
    avg_confidence_score: float
    response_accuracy: float


@router.get("/conversations", response_model=ConversationMetrics)
async def get_conversation_metrics(
    start_date: datetime,
    end_date: datetime
):
    """
    Konuşma metriklerini getir
    """
    try:
        # Placeholder data - replace with actual database queries
        metrics = ConversationMetrics(
            total_conversations=1250,
            avg_conversation_length=5.8,
            avg_response_time=1.2,
            satisfaction_rate=0.92
        )
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting conversation metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/{product_id}", response_model=ProductMetrics)
async def get_product_metrics(
    product_id: str,
    days: int = 30
):
    """
    Ürün bazlı metrikleri getir
    """
    try:
        # Placeholder data
        metrics = ProductMetrics(
            product_id=product_id,
            total_inquiries=456,
            configuration_requests=89,
            conversion_rate=0.35,
            top_questions=[
                "Pricing information",
                "Integration options",
                "Setup requirements",
                "API documentation",
                "Support availability"
            ]
        )
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting product metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agent/performance", response_model=AgentPerformance)
async def get_agent_performance(
    start_date: datetime,
    end_date: datetime
):
    """
    Agent performans metriklerini getir
    """
    try:
        # Placeholder data
        performance = AgentPerformance(
            total_interactions=3450,
            successful_resolutions=3120,
            escalations=89,
            avg_confidence_score=0.87,
            response_accuracy=0.91
        )
        
        return performance
        
    except Exception as e:
        logger.error(f"Error getting agent performance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_dashboard_summary():
    """
    Dashboard özet bilgilerini getir
    """
    try:
        return {
            "overview": {
                "active_products": 12,
                "total_conversations_today": 89,
                "avg_satisfaction": 0.92,
                "active_sessions": 23
            },
            "trends": {
                "conversations_trend": [45, 52, 48, 67, 89],
                "conversion_trend": [0.32, 0.35, 0.38, 0.36, 0.35]
            },
            "alerts": [
                {
                    "type": "warning",
                    "message": "Response time increased by 15%",
                    "timestamp": datetime.utcnow()
                }
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting dashboard summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
