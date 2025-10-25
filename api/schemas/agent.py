from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AgentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=1000)
    persona_role: str = Field(default="")
    persona_tone: str = Field(default="professional")
    persona_instructions: str = Field(default="")
    persona_constraints: str = Field(default="")

class AgentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    persona_role: Optional[str] = None
    persona_tone: Optional[str] = None
    persona_instructions: Optional[str] = None
    persona_constraints: Optional[str] = None
    status: Optional[str] = None

class AgentResponse(BaseModel):
    id: str
    name: str
    description: str
    persona_role: str
    persona_tone: str
    persona_instructions: str
    persona_constraints: str
    status: str
    document_count: int
    endpoint_count: int
    created_at: datetime
    updated_at: datetime

class EndpointCreate(BaseModel):
    name: str
    method: str
    url: str
    description: str = ""
    request_example: str = ""
    response_example: str = ""

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
