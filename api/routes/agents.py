from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
import logging
from api.schemas.agent import (
    AgentCreate, AgentUpdate, AgentResponse, 
    EndpointCreate, ChatRequest
)
from agent.storage.agent_store import agent_store
from agent.knowledge_base.knowledge_manager import KnowledgeManager
from agent.qa_engine.qa_processor import QAProcessor
from core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize managers
knowledge_manager = KnowledgeManager()
qa_processor = QAProcessor()

@router.post("/agents", response_model=AgentResponse)
async def create_agent(agent: AgentCreate):
    """Create a new agent"""
    try:
        agent_data = agent.model_dump()
        created_agent = agent_store.create_agent(agent_data)
        
        # Create collection in ChromaDB for this agent
        collection_name = f"agent_{created_agent['id']}"
        knowledge_manager.create_collection(collection_name)
        
        logger.info(f"Created agent: {created_agent['id']} - {created_agent['name']}")
        
        return AgentResponse(
            id=created_agent['id'],
            name=created_agent['name'],
            description=created_agent['description'],
            persona_role=created_agent['persona_role'],
            persona_tone=created_agent['persona_tone'],
            persona_instructions=created_agent['persona_instructions'],
            persona_constraints=created_agent['persona_constraints'],
            status=created_agent['status'],
            document_count=len(created_agent.get('documents', [])),
            endpoint_count=len(created_agent.get('endpoints', [])),
            created_at=created_agent['created_at'],
            updated_at=created_agent['updated_at']
        )
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents", response_model=List[AgentResponse])
async def list_agents():
    """List all agents"""
    try:
        agents = agent_store.list_agents()
        return [
            AgentResponse(
                id=agent['id'],
                name=agent['name'],
                description=agent['description'],
                persona_role=agent.get('persona_role', ''),
                persona_tone=agent.get('persona_tone', 'professional'),
                persona_instructions=agent.get('persona_instructions', ''),
                persona_constraints=agent.get('persona_constraints', ''),
                status=agent.get('status', 'active'),
                document_count=len(agent.get('documents', [])),
                endpoint_count=len(agent.get('endpoints', [])),
                created_at=agent['created_at'],
                updated_at=agent['updated_at']
            )
            for agent in agents
        ]
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Get a specific agent"""
    agent = agent_store.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return AgentResponse(
        id=agent['id'],
        name=agent['name'],
        description=agent['description'],
        persona_role=agent.get('persona_role', ''),
        persona_tone=agent.get('persona_tone', 'professional'),
        persona_instructions=agent.get('persona_instructions', ''),
        persona_constraints=agent.get('persona_constraints', ''),
        status=agent.get('status', 'active'),
        document_count=len(agent.get('documents', [])),
        endpoint_count=len(agent.get('endpoints', [])),
        created_at=agent['created_at'],
        updated_at=agent['updated_at']
    )

@router.put("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, agent_update: AgentUpdate):
    """Update an agent"""
    update_data = agent_update.model_dump(exclude_unset=True)
    updated_agent = agent_store.update_agent(agent_id, update_data)
    
    if not updated_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return AgentResponse(
        id=updated_agent['id'],
        name=updated_agent['name'],
        description=updated_agent['description'],
        persona_role=updated_agent.get('persona_role', ''),
        persona_tone=updated_agent.get('persona_tone', 'professional'),
        persona_instructions=updated_agent.get('persona_instructions', ''),
        persona_constraints=updated_agent.get('persona_constraints', ''),
        status=updated_agent.get('status', 'active'),
        document_count=len(updated_agent.get('documents', [])),
        endpoint_count=len(updated_agent.get('endpoints', [])),
        created_at=updated_agent['created_at'],
        updated_at=updated_agent['updated_at']
    )

@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent"""
    success = agent_store.delete_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Delete ChromaDB collection
    try:
        collection_name = f"agent_{agent_id}"
        knowledge_manager.delete_collection(collection_name)
    except:
        pass
    
    return {"message": "Agent deleted successfully"}

@router.post("/agents/{agent_id}/documents")
async def upload_document(
    agent_id: str,
    file: UploadFile = File(...)
):
    """Upload and process a document for an agent"""
    agent = agent_store.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        # Read file content
        content = await file.read()
        
        # Try to decode as UTF-8, if fails treat as binary
        try:
            text_content = content.decode('utf-8')
        except UnicodeDecodeError:
            # For binary files like PDFs, we would need a PDF parser
            # For now, just skip binary files
            raise HTTPException(
                status_code=400, 
                detail="Only text files are supported (TXT, MD). PDF support coming soon."
            )
        
        # Process and add to ChromaDB
        collection_name = f"agent_{agent_id}"
        doc_id = knowledge_manager.add_document(
            collection_name=collection_name,
            content=text_content,
            metadata={
                "filename": file.filename,
                "agent_id": agent_id
            }
        )
        
        # Store document metadata
        document = {
            "id": doc_id,
            "name": file.filename,
            "size": len(content),
            "type": file.content_type,
            "status": "ready",
            "uploaded_at": datetime.now().isoformat()
        }
        
        agent_store.add_document(agent_id, document)
        
        logger.info(f"Uploaded document {file.filename} for agent {agent_id}")
        return {"message": "Document uploaded successfully", "document": document}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")

@router.post("/agents/{agent_id}/endpoints")
async def add_endpoint(agent_id: str, endpoint: EndpointCreate):
    """Add an endpoint to an agent"""
    agent = agent_store.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    endpoint_data = endpoint.model_dump()
    endpoint_data["id"] = str(uuid.uuid4())
    
    agent_store.add_endpoint(agent_id, endpoint_data)
    
    return {"message": "Endpoint added successfully", "endpoint": endpoint_data}

@router.post("/agents/{agent_id}/chat")
async def chat_with_agent(agent_id: str, chat_request: ChatRequest):
    """Chat with a specific agent"""
    agent = agent_store.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        # Build system prompt
        system_prompt = f"""You are {agent['name']}. {agent['description']}

Role: {agent.get('persona_role', 'AI Assistant')}
Tone: {agent.get('persona_tone', 'professional')}

Instructions:
{agent.get('persona_instructions', 'Help users with their questions.')}

Constraints:
{agent.get('persona_constraints', 'Be helpful and accurate.')}
"""
        
        # Get relevant context from documents
        collection_name = f"agent_{agent_id}"
        context = knowledge_manager.search(
            collection_name=collection_name,
            query=chat_request.message,
            n_results=3
        )
        
        # Generate response
        response = qa_processor.process_query(
            query=chat_request.message,
            context=context,
            system_prompt=system_prompt
        )
        
        return {
            "response": response,
            "agent_id": agent_id,
            "agent_name": agent['name']
        }
        
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from datetime import datetime
import uuid
