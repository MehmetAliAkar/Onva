"""
Agent API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from agent.knowledge_base.knowledge_manager import KnowledgeManager
from agent.qa_engine.qa_processor import QAProcessor
from agent.config_manager.config_handler import ConfigHandler
from core.logging import logger

router = APIRouter()

# Initialize components
knowledge_manager = KnowledgeManager()
qa_processor = QAProcessor()
config_handler = ConfigHandler()


class ChatRequest(BaseModel):
    """Chat request model"""
    product_id: str
    message: str
    context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    confidence: float
    suggestions: Optional[List[str]] = None
    product_config: Optional[Dict[str, Any]] = None


class ConfigRequest(BaseModel):
    """Configuration request model"""
    product_id: str
    user_inputs: Dict[str, Any]
    requirements: Optional[List[str]] = None


class ConfigResponse(BaseModel):
    """Configuration response model"""
    product_id: str
    configuration: Dict[str, Any]
    estimated_price: Optional[float] = None
    setup_steps: List[str]


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Agent ile sohbet et - Ürün soruları, bilgi talebi
    """
    try:
        logger.info(f"Chat request for product: {request.product_id}")
        
        # Get product knowledge
        product_knowledge = await knowledge_manager.get_product_knowledge(
            request.product_id
        )
        
        if not product_knowledge:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Process question with QA engine
        response = await qa_processor.process_question(
            question=request.message,
            product_knowledge=product_knowledge,
            context=request.context,
            session_id=request.session_id
        )
        
        return ChatResponse(
            response=response["answer"],
            confidence=response["confidence"],
            suggestions=response.get("suggestions"),
            product_config=response.get("config_suggestion")
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/configure", response_model=ConfigResponse)
async def configure_product(request: ConfigRequest):
    """
    Ürünü kullanıcı girdilerine göre yapılandır
    """
    try:
        logger.info(f"Configuration request for product: {request.product_id}")
        
        # Generate configuration
        config = await config_handler.generate_configuration(
            product_id=request.product_id,
            user_inputs=request.user_inputs,
            requirements=request.requirements
        )
        
        return ConfigResponse(
            product_id=request.product_id,
            configuration=config["settings"],
            estimated_price=config.get("pricing"),
            setup_steps=config["setup_steps"]
        )
        
    except Exception as e:
        logger.error(f"Error in configure endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/product/{product_id}/capabilities")
async def get_product_capabilities(product_id: str):
    """
    Ürün yeteneklerini ve özelliklerini getir
    """
    try:
        capabilities = await knowledge_manager.get_capabilities(product_id)
        return {
            "product_id": product_id,
            "capabilities": capabilities
        }
    except Exception as e:
        logger.error(f"Error getting capabilities: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-requirements")
async def analyze_requirements(
    product_id: str,
    requirements: List[str]
):
    """
    Müşteri gereksinimlerini analiz et ve uygun yapılandırma öner
    """
    try:
        analysis = await config_handler.analyze_requirements(
            product_id=product_id,
            requirements=requirements
        )
        
        return {
            "product_id": product_id,
            "requirements_analysis": analysis["analysis"],
            "recommended_config": analysis["recommendation"],
            "compatibility_score": analysis["score"]
        }
        
    except Exception as e:
        logger.error(f"Error analyzing requirements: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
