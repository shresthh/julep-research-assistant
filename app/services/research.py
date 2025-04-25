"""
Research service implementation.

This module contains the business logic for performing research using the Julep AI agent.
"""

from typing import Dict, Any

from app.core.agent import agent_manager
from app.core.logging import setup_logger

# Set up logger for this module
logger = setup_logger(__name__)


class ResearchError(Exception):
    """Base exception for research service errors."""
    pass


class AgentSessionError(ResearchError):
    """Exception raised when there's an error with agent sessions."""
    pass


class ResearchResponseError(ResearchError):
    """Exception raised when there's an error with research responses."""
    pass


class ResearchService:
    """
    Service for handling research requests.
    """
    
    @staticmethod
    async def perform_research(topic: str, output_format: str) -> Dict[str, Any]:
        """
        Perform research on the given topic and format the results.
        
        Args:
            topic (str): The research topic.
            output_format (str): The desired output format.
            
        Returns:
            Dict[str, Any]: Dictionary containing the research results.
            
        Raises:
            AgentSessionError: If there's an error creating a session.
            ResearchResponseError: If there's an error getting a response.
            ResearchError: For other research-related errors.
        """
        logger.info(f"Starting research on topic: '{topic}' in format: '{output_format}'")
        
        try:
            # Create a descriptive situation for the session
            situation = (
                f"User wants to research about '{topic}' and receive "
                f"results in '{output_format}' format."
            )
            
            # Create a session for this research request
            try:
                session = agent_manager.create_session(situation=situation)
                logger.info(f"Created research session with ID: {session.id}")
            except Exception as session_error:
                error_msg = f"Failed to create research session: {str(session_error)}"
                logger.error(error_msg)
                raise AgentSessionError(error_msg) from session_error
            
            # Construct the user message
            prompt = (
                f"Please research the topic '{topic}' and provide the "
                f"information in '{output_format}' format."
            )
            
            # Send the research request to the agent
            try:
                messages = [{"role": "user", "content": prompt}]
                response = agent_manager.chat(session.id, messages)
                logger.info("Successfully received research response")
            except Exception as response_error:
                error_msg = f"Failed to get research response: {str(response_error)}"
                logger.error(error_msg)
                raise ResearchResponseError(error_msg) from response_error
            
            # Validate response structure
            if not hasattr(response, 'choices') or not response.choices:
                error_msg = "Invalid response format: missing 'choices'"
                logger.error(error_msg)
                raise ResearchResponseError(error_msg)
            
            if not hasattr(response.choices[0], 'message') or not hasattr(response.choices[0].message, 'content'):
                error_msg = "Invalid response format: missing 'message.content'"
                logger.error(error_msg)
                raise ResearchResponseError(error_msg)
            
            # Extract and return the research results
            result = {
                "topic": topic,
                "format": output_format,
                "result": response.choices[0].message.content
            }
            
            logger.info(f"Research completed successfully for topic: '{topic}'")
            return result
            
        except (AgentSessionError, ResearchResponseError):
            # Re-raise specific exceptions that we've already logged
            raise
        except Exception as e:
            # Log and wrap any other exceptions
            error_msg = f"Unexpected error in research process: {str(e)}"
            logger.error(error_msg)
            raise ResearchError(error_msg) from e


# Create a singleton instance
research_service = ResearchService()