"""
Jira Integration Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jira import JIRA
import logging
from core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

class JiraTaskRequest(BaseModel):
    text: str
    project_key: str = "COMP"  # Default project key
    issue_type: str = "Task"  # Task, Bug, Story, etc.

class JiraTaskResponse(BaseModel):
    success: bool
    task_key: str
    task_url: str
    message: str

@router.post("/jira/create-task", response_model=JiraTaskResponse)
async def create_jira_task(request: JiraTaskRequest):
    """
    Create a Jira task from text
    
    Args:
        text: Task description/summary
        project_key: Jira project key (e.g., 'COMP', 'PROJ')
        issue_type: Type of issue (Task, Bug, Story, etc.)
    
    Returns:
        Task details including key and URL
    """
    # Check if Jira is configured
    if not settings.JIRA_SERVER or not settings.JIRA_EMAIL or not settings.JIRA_API_TOKEN:
        raise HTTPException(
            status_code=400,
            detail="Jira is not configured. Please set JIRA_SERVER, JIRA_EMAIL, and JIRA_API_TOKEN in .env file"
        )
    
    try:
        # Initialize Jira client
        jira = JIRA(
            server=settings.JIRA_SERVER,
            basic_auth=(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN)
        )
        
        # Create issue
        issue_dict = {
            'project': {'key': request.project_key},
            'summary': request.text,
            'description': request.text,
            'issuetype': {'name': request.issue_type},
        }
        
        new_issue = jira.create_issue(fields=issue_dict)
        
        task_url = f"{settings.JIRA_SERVER}/browse/{new_issue.key}"
        
        logger.info(f"Created Jira task: {new_issue.key}")
        
        return JiraTaskResponse(
            success=True,
            task_key=new_issue.key,
            task_url=task_url,
            message=f"Task {new_issue.key} created successfully"
        )
        
    except Exception as e:
        logger.error(f"Error creating Jira task: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create Jira task: {str(e)}"
        )

@router.get("/jira/test-connection")
async def test_jira_connection():
    """Test Jira connection"""
    # Check if Jira is configured
    if not settings.JIRA_SERVER or not settings.JIRA_EMAIL or not settings.JIRA_API_TOKEN:
        raise HTTPException(
            status_code=400,
            detail="Jira is not configured. Please set JIRA_SERVER, JIRA_EMAIL, and JIRA_API_TOKEN in .env file"
        )
    
    try:
        jira = JIRA(
            server=settings.JIRA_SERVER,
            basic_auth=(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN)
        )
        
        # Get current user to test connection
        current_user = jira.current_user()
        
        return {
            "success": True,
            "message": "Jira connection successful",
            "user": current_user
        }
        
    except Exception as e:
        logger.error(f"Jira connection failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Jira connection failed: {str(e)}"
        )
