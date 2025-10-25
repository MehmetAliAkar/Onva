"""
Agent module initialization
"""
from .knowledge_base import KnowledgeManager
from .qa_engine import QAProcessor
from .config_manager import ConfigHandler

__all__ = ["KnowledgeManager", "QAProcessor", "ConfigHandler"]
