"""
Julep AI agent creation and management.

This module handles creation and management of the Julep AI research assistant agent.
"""

from typing import Dict, Any, Optional

from julep import Julep

from app.core.config import get_settings
from app.core.logging import setup_logger


# Set up logger for this module
logger = setup_logger(__name__)


class JulepAgentManager:
    """
    Manages the Julep AI agent for research assistance.
    """
    
    def __init__(self):
        """Initialize the Julep client and agent reference."""
        self.settings = get_settings()
        self.julep = Julep(api_key=self.settings.JULEP_API_KEY)
        self._agent_id: Optional[str] = None
    
    @property
    def agent_id(self) -> str:
        """
        Get the agent ID, creating the agent if it doesn't exist yet.
        
        Returns:
            str: The ID of the research assistant agent.
            
        Raises:
            Exception: If there is an error creating the agent.
        """
        if self._agent_id is None:
            try:
                agent = self.create_research_agent()
                self._agent_id = agent.id
            except Exception as e:
                logger.error(f"Failed to get agent ID: {str(e)}")
                raise
        return self._agent_id
    
    def create_research_agent(self) -> Any:
        """
        Create a research assistant agent in Julep with Wikipedia tool integration.
        
        Returns:
            Any: The created agent object from Julep.
            
        Raises:
            Exception: If there's an error in creating the agent or attaching tools.
        """
        try:
            # Create the base agent
            logger.info("Creating research assistant agent...")
            agent = self.julep.agents.create(
                name="Research Assistant",
                about="An AI research assistant that provides information in requested formats",
                instructions=[
                    # Layer 1: Base Instruction - Core role
                    "You are a helpful research assistant. Your goal is to find concise information on topics provided by the user.",
                    
                    # Layer 2: Task Instruction - Primary task
                    "When given a topic and an output format (e.g., 'summary', 'bullet points', 'short report'), you must gather relevant information and structure it according to the requested format.",
                    
                    # Layer 3: Persona/Formatting Instruction - Tone and constraints
                    "Maintain a neutral, objective tone. Strictly adhere to the requested output format. Keep summaries to 3-4 sentences, bullet points concise (max 5 points), and short reports under 150 words. If you cannot find reliable information, state that clearly."
                ],
                model=self.settings.JULEP_MODEL,
            )
            
            logger.info(f"Successfully created agent with ID: {agent.id}")
            
            # Attach the Wikipedia search tool to the agent
            try:
                logger.info(f"Attaching Wikipedia tool to agent: {agent.id}")
                self.julep.agents.tools.create(
                    agent_id=agent.id,
                    **{
                        "name": "wikipedia_search",
                        "type": "integration",
                        "integration": {
                            "provider": "wikipedia",
                        }
                    }
                )
                logger.info(f"Successfully attached Wikipedia tool to agent: {agent.id}")
            except Exception as tool_error:
                logger.warning(f"Error attaching Wikipedia tool to agent: {str(tool_error)}")
                logger.warning("Continuing with agent creation without Wikipedia tool")
                # We'll continue even if tool attachment fails, as the base agent can still function
                
            return agent
            
        except Exception as e:
            error_message = f"Failed to create research agent: {str(e)}"
            logger.error(error_message)
            # Re-raise the exception to be handled by the caller
            raise
    
    def create_session(self, situation: str) -> Any:
        """
        Create a new session with the research assistant agent.
        
        Args:
            situation (str): Description of the user's situation.
            
        Returns:
            Any: The created session object from Julep.
            
        Raises:
            Exception: If there's an error creating the session.
        """
        try:
            logger.info(f"Creating session with situation: {situation}")
            session = self.julep.sessions.create(
                agent=self.agent_id,
                situation=situation,
            )
            logger.info(f"Session created successfully with ID: {session.id}")
            return session
        except Exception as e:
            logger.error(f"Failed to create session: {str(e)}")
            raise
    
    def chat(self, session_id: str, messages: list) -> Any:
        """
        Send a message to the agent and get a response.
        
        Args:
            session_id (str): ID of the session to use.
            messages (list): List of message objects to send.
            
        Returns:
            Any: The response from the agent.
            
        Raises:
            Exception: If there's an error in the chat process.
        """
        try:
            logger.info(f"Sending messages to session: {session_id}")
            response = self.julep.sessions.chat(
                session_id=session_id,
                messages=messages
            )
            logger.info("Received response from Julep")
            return response
        except Exception as e:
            logger.error(f"Failed to chat with agent: {str(e)}")
            raise


# Create a singleton instance
agent_manager = JulepAgentManager()