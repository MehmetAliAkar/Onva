"""
Knowledge Manager - Document and vector database management with ChromaDB
"""
from typing import Dict, Any, Optional, List
import json
import uuid
from core.logging import logger
import chromadb

class KnowledgeManager:
    """
    Manages knowledge base with ChromaDB vector database
    - Stores and retrieves product information
    - Indexes documents
    - Performs vector search for relevant information
    """
    
    def __init__(self):
        self.knowledge_base: Dict[str, Dict[str, Any]] = {}
        
        # Initialize ChromaDB with new persistent client
        try:
            self.chroma_client = chromadb.PersistentClient(path="./data/chroma")
            logger.info("KnowledgeManager initialized with ChromaDB")
        except Exception as e:
            logger.warning(f"ChromaDB initialization failed, using in-memory: {e}")
            self.chroma_client = chromadb.Client()
            logger.info("KnowledgeManager initialized with in-memory ChromaDB")
    
    def create_collection(self, collection_name: str):
        """Create a new collection in ChromaDB"""
        try:
            collection = self.chroma_client.get_or_create_collection(
                name=collection_name,
                metadata={"description": f"Knowledge base for {collection_name}"}
            )
            logger.info(f"Created/retrieved collection: {collection_name}")
            return collection
        except Exception as e:
            logger.error(f"Error creating collection {collection_name}: {e}")
            raise
    
    def delete_collection(self, collection_name: str):
        """Delete a collection from ChromaDB"""
        try:
            self.chroma_client.delete_collection(name=collection_name)
            logger.info(f"Deleted collection: {collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection {collection_name}: {e}")
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        
        return chunks
    
    def add_document(self, collection_name: str, content: str, metadata: Dict = None) -> str:
        """
        Add a document to the collection with chunking
        
        Args:
            collection_name: Name of the collection
            content: Document content
            metadata: Additional metadata
            
        Returns:
            Document ID
        """
        try:
            collection = self.chroma_client.get_collection(name=collection_name)
            
            # Chunk the document
            chunks = self.chunk_text(content)
            doc_id = str(uuid.uuid4())
            
            # Add each chunk to the collection
            ids = []
            documents = []
            metadatas = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id}_chunk_{i}"
                ids.append(chunk_id)
                documents.append(chunk)
                
                chunk_metadata = metadata.copy() if metadata else {}
                chunk_metadata.update({
                    "doc_id": doc_id,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                })
                metadatas.append(chunk_metadata)
            
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
            logger.info(f"Added document {doc_id} with {len(chunks)} chunks to {collection_name}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error adding document to {collection_name}: {e}")
            raise
    
    def search(self, collection_name: str, query: str, n_results: int = 3) -> str:
        """
        Search for relevant documents in the collection
        
        Args:
            collection_name: Name of the collection
            query: Search query
            n_results: Number of results to return
            
        Returns:
            Concatenated relevant context
        """
        try:
            collection = self.chroma_client.get_collection(name=collection_name)
            
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if not results['documents'] or not results['documents'][0]:
                return ""
            
            # Concatenate results
            context = "\n\n".join(results['documents'][0])
            logger.info(f"Found {len(results['documents'][0])} relevant chunks for query in {collection_name}")
            
            return context
            
        except Exception as e:
            logger.error(f"Error searching in {collection_name}: {e}")
            return ""
    
    async def get_product_knowledge(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Ürün bilgisini getir
        
        Args:
            product_id: Ürün ID'si
            
        Returns:
            Ürün bilgi tabanı
        """
        try:
            if product_id in self.knowledge_base:
                return self.knowledge_base[product_id]
            
            # Varsayılan bilgi tabanı yapısı
            default_knowledge = {
                "product_id": product_id,
                "name": "Sample Product",
                "description": "Product description",
                "features": [],
                "technical_specs": {},
                "use_cases": [],
                "integration_guide": {},
                "faq": [],
                "pricing": {}
            }
            
            return default_knowledge
            
        except Exception as e:
            logger.error(f"Error getting product knowledge: {str(e)}")
            return None
    
    async def add_product_knowledge(
        self,
        product_id: str,
        knowledge_data: Dict[str, Any]
    ) -> bool:
        """
        Yeni ürün bilgisi ekle
        
        Args:
            product_id: Ürün ID'si
            knowledge_data: Ürün bilgi verisi
            
        Returns:
            Başarı durumu
        """
        try:
            self.knowledge_base[product_id] = knowledge_data
            logger.info(f"Added knowledge for product: {product_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding product knowledge: {str(e)}")
            return False
    
    async def update_product_knowledge(
        self,
        product_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """
        Ürün bilgisini güncelle
        
        Args:
            product_id: Ürün ID'si
            updates: Güncellenecek alanlar
            
        Returns:
            Başarı durumu
        """
        try:
            if product_id in self.knowledge_base:
                self.knowledge_base[product_id].update(updates)
                logger.info(f"Updated knowledge for product: {product_id}")
                return True
            else:
                logger.warning(f"Product not found: {product_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating product knowledge: {str(e)}")
            return False
    
    async def get_capabilities(self, product_id: str) -> List[str]:
        """
        Ürün yeteneklerini listele
        
        Args:
            product_id: Ürün ID'si
            
        Returns:
            Yetenek listesi
        """
        try:
            knowledge = await self.get_product_knowledge(product_id)
            if knowledge:
                return knowledge.get("features", [])
            return []
            
        except Exception as e:
            logger.error(f"Error getting capabilities: {str(e)}")
            return []
    
    async def search_knowledge(
        self,
        product_id: str,
        query: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Bilgi tabanında arama yap
        
        Args:
            product_id: Ürün ID'si
            query: Arama sorgusu
            category: Kategori filtresi (faq, features, etc.)
            
        Returns:
            Arama sonuçları
        """
        try:
            knowledge = await self.get_product_knowledge(product_id)
            if not knowledge:
                return []
            
            results = []
            
            # Simple keyword search (replace with vector search in production)
            query_lower = query.lower()
            
            if category == "faq" or category is None:
                faq = knowledge.get("faq", [])
                for item in faq:
                    if query_lower in item.get("question", "").lower():
                        results.append({
                            "type": "faq",
                            "content": item,
                            "relevance": 0.9
                        })
            
            if category == "features" or category is None:
                features = knowledge.get("features", [])
                for feature in features:
                    if query_lower in str(feature).lower():
                        results.append({
                            "type": "feature",
                            "content": feature,
                            "relevance": 0.8
                        })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching knowledge: {str(e)}")
            return []
    
    async def index_documentation(
        self,
        product_id: str,
        documentation: str
    ) -> bool:
        """
        Dokümantasyonu indexle (gelecekte vektör DB kullanılacak)
        
        Args:
            product_id: Ürün ID'si
            documentation: Dokümantasyon metni
            
        Returns:
            Başarı durumu
        """
        try:
            # TODO: Implement vector database indexing
            # For now, just store in memory
            if product_id in self.knowledge_base:
                self.knowledge_base[product_id]["documentation"] = documentation
                logger.info(f"Indexed documentation for product: {product_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error indexing documentation: {str(e)}")
            return False
