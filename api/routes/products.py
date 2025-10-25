"""
Products API endpoints
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

from core.logging import logger

router = APIRouter()


class Product(BaseModel):
    """Product model"""
    id: str
    name: str
    description: str
    category: str
    features: List[str]
    pricing_model: str
    integration_options: List[str]
    documentation_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ProductCreate(BaseModel):
    """Product creation model"""
    name: str
    description: str
    category: str
    features: List[str]
    pricing_model: str
    integration_options: List[str]
    documentation_url: Optional[str] = None
    knowledge_base: Dict[str, Any]


class ProductUpdate(BaseModel):
    """Product update model"""
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    pricing_model: Optional[str] = None
    integration_options: Optional[List[str]] = None
    documentation_url: Optional[str] = None
    knowledge_base: Optional[Dict[str, Any]] = None


# Temporary in-memory storage (replace with database)
products_db: Dict[str, Product] = {}


@router.get("/", response_model=List[Product])
async def list_products(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Tüm ürünleri listele
    """
    try:
        products = list(products_db.values())
        
        if category:
            products = [p for p in products if p.category == category]
        
        return products[skip:skip + limit]
        
    except Exception as e:
        logger.error(f"Error listing products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """
    Yeni ürün ekle
    """
    try:
        product_id = f"prod_{len(products_db) + 1}"
        now = datetime.utcnow()
        
        new_product = Product(
            id=product_id,
            name=product.name,
            description=product.description,
            category=product.category,
            features=product.features,
            pricing_model=product.pricing_model,
            integration_options=product.integration_options,
            documentation_url=product.documentation_url,
            created_at=now,
            updated_at=now
        )
        
        products_db[product_id] = new_product
        logger.info(f"Created product: {product_id}")
        
        return new_product
        
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """
    Belirli bir ürünü getir
    """
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return products_db[product_id]


@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: str, product_update: ProductUpdate):
    """
    Ürün bilgilerini güncelle
    """
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    try:
        existing_product = products_db[product_id]
        update_data = product_update.model_dump(exclude_unset=True)
        
        updated_product = existing_product.model_copy(update=update_data)
        updated_product.updated_at = datetime.utcnow()
        
        products_db[product_id] = updated_product
        logger.info(f"Updated product: {product_id}")
        
        return updated_product
        
    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str):
    """
    Ürünü sil
    """
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    del products_db[product_id]
    logger.info(f"Deleted product: {product_id}")
    
    return None
