from typing import Dict, List, Optional
from datetime import datetime
import uuid
import json
from pathlib import Path

class AgentStore:
    def __init__(self):
        self.agents: Dict[str, dict] = {}
        self.storage_path = Path("data/agents")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._load_agents()
    
    def _load_agents(self):
        """Load agents from disk"""
        for agent_file in self.storage_path.glob("*.json"):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    agent = json.load(f)
                    self.agents[agent['id']] = agent
            except Exception as e:
                print(f"Error loading agent {agent_file}: {e}")
    
    def _save_agent(self, agent_id: str):
        """Save agent to disk"""
        agent = self.agents[agent_id]
        agent_file = self.storage_path / f"{agent_id}.json"
        with open(agent_file, 'w', encoding='utf-8') as f:
            json.dump(agent, f, indent=2, default=str)
    
    def create_agent(self, agent_data: dict) -> dict:
        """Create a new agent"""
        agent_id = str(uuid.uuid4())
        now = datetime.now()
        
        agent = {
            "id": agent_id,
            "name": agent_data["name"],
            "description": agent_data["description"],
            "persona_role": agent_data.get("persona_role", ""),
            "persona_tone": agent_data.get("persona_tone", "professional"),
            "persona_instructions": agent_data.get("persona_instructions", ""),
            "persona_constraints": agent_data.get("persona_constraints", ""),
            "status": "active",
            "documents": [],
            "endpoints": [],
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
        
        self.agents[agent_id] = agent
        self._save_agent(agent_id)
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[dict]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[dict]:
        """List all agents"""
        return list(self.agents.values())
    
    def update_agent(self, agent_id: str, update_data: dict) -> Optional[dict]:
        """Update an agent"""
        if agent_id not in self.agents:
            return None
        
        agent = self.agents[agent_id]
        for key, value in update_data.items():
            if value is not None and key != "id":
                agent[key] = value
        
        agent["updated_at"] = datetime.now().isoformat()
        self._save_agent(agent_id)
        return agent
    
    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent"""
        if agent_id not in self.agents:
            return False
        
        del self.agents[agent_id]
        agent_file = self.storage_path / f"{agent_id}.json"
        if agent_file.exists():
            agent_file.unlink()
        return True
    
    def add_document(self, agent_id: str, document: dict) -> bool:
        """Add a document to an agent"""
        if agent_id not in self.agents:
            return False
        
        self.agents[agent_id]["documents"].append(document)
        self.agents[agent_id]["updated_at"] = datetime.now().isoformat()
        self._save_agent(agent_id)
        return True
    
    def add_endpoint(self, agent_id: str, endpoint: dict) -> bool:
        """Add an endpoint to an agent"""
        if agent_id not in self.agents:
            return False
        
        self.agents[agent_id]["endpoints"].append(endpoint)
        self.agents[agent_id]["updated_at"] = datetime.now().isoformat()
        self._save_agent(agent_id)
        return True

# Global instance
agent_store = AgentStore()
