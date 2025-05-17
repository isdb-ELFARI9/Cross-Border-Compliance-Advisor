"""
Orchestrator service - manages access to all orchestrators.
"""

import asyncio
import sys
import os
from typing import Dict, Any, Optional

from api.core.logging import logger

class OrchestratorService:
    """Service to manage all orchestrators."""
    
    # Global references to orchestrators
    qa_transform_orchestrator = None
    regulation_revision_orchestrator = None
    update_revision_orchestrator = None
    
    @classmethod
    async def initialize(cls):
        """Initialize all orchestrators."""
        # Ensure the src directory is in the path
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if project_root not in sys.path:
            sys.path.append(project_root)
            logger.info(f"Added {project_root} to Python path")
        
        # Initialize each orchestrator separately to avoid one failure affecting others
        await cls._init_qa_transform()
        await cls._init_regulation_revision()
        await cls._init_update_revision()
        
    @classmethod
    async def _init_qa_transform(cls):
        """Initialize QA Transform orchestrator."""
        try:
            # Import orchestrator
            from src.orchestators.orch_qa_transform_aaoifi import QATransformOrchestrator
            
            # Initialize orchestrator
            logger.info("Initializing QA Transform Orchestrator...")
            cls.qa_transform_orchestrator = QATransformOrchestrator()
            logger.info("QA Transform Orchestrator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize QA Transform Orchestrator: {str(e)}")
            cls.qa_transform_orchestrator = None
    
    @classmethod
    async def _init_regulation_revision(cls):
        """Initialize Regulation Revision orchestrator."""
        try:
            # Import orchestrator
            from src.orchestators.orch_drafting_shariah_compliant_regulations import RegulationRevisionOrchestrator
            
            # Initialize orchestrator
            logger.info("Initializing Regulation Revision Orchestrator...")
            cls.regulation_revision_orchestrator = RegulationRevisionOrchestrator()
            logger.info("Regulation Revision Orchestrator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Regulation Revision Orchestrator: {str(e)}")
            cls.regulation_revision_orchestrator = None
    
    @classmethod
    async def _init_update_revision(cls):
        """Initialize Update Revision orchestrator."""
        try:
            # Import orchestrator
            from src.orchestators.orch_revision_updated_regulation_framework import UpdateRevisionOrchestrator
            
            # Initialize orchestrator
            logger.info("Initializing Update Revision Orchestrator...")
            cls.update_revision_orchestrator = UpdateRevisionOrchestrator()
            logger.info("Update Revision Orchestrator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Update Revision Orchestrator: {str(e)}")
            cls.update_revision_orchestrator = None
    
    @classmethod
    def cleanup(cls):
        """Clean up orchestrators."""
        cls.qa_transform_orchestrator = None
        cls.regulation_revision_orchestrator = None
        cls.update_revision_orchestrator = None
    
    @classmethod
    def get_status(cls) -> Dict[str, bool]:
        """Get status of all orchestrators."""
        return {
            "qa_transform": cls.qa_transform_orchestrator is not None,
            "regulation_revision": cls.regulation_revision_orchestrator is not None,
            "update_revision": cls.update_revision_orchestrator is not None
        }
    
    @classmethod
    def get_qa_transform_orchestrator(cls):
        """Get QA Transform orchestrator."""
        return cls.qa_transform_orchestrator
    
    @classmethod
    def get_regulation_revision_orchestrator(cls):
        """Get Regulation Revision orchestrator."""
        return cls.regulation_revision_orchestrator
    
    @classmethod
    def get_update_revision_orchestrator(cls):
        """Get Update Revision orchestrator."""
        return cls.update_revision_orchestrator
