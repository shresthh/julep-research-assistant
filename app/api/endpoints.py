"""
API endpoint definitions.

This module contains the FastAPI application and endpoint definitions.
"""

from fastapi import FastAPI, HTTPException, Depends, Body, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.models import ResearchRequest, ResearchResponse
from app.core.config import get_settings, Settings
from app.core.logging import setup_logger
from app.services.research import (
    research_service, 
    ResearchError, 
    AgentSessionError, 
    ResearchResponseError
)

# Set up logger for this module
logger = setup_logger(__name__)


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: The configured FastAPI application.
    """
    settings = get_settings()
    
    application = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
    )
    
    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return application


app = create_application()


# Exception handlers
@app.exception_handler(AgentSessionError)
async def handle_agent_session_error(request, exc):
    """Handle agent session errors."""
    logger.error(f"AgentSessionError: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": f"Agent session error: {str(exc)}"}
    )


@app.exception_handler(ResearchResponseError)
async def handle_research_response_error(request, exc):
    """Handle research response errors."""
    logger.error(f"ResearchResponseError: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Research response error: {str(exc)}"}
    )


@app.exception_handler(ResearchError)
async def handle_research_error(request, exc):
    """Handle general research errors."""
    logger.error(f"ResearchError: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Research error: {str(exc)}"}
    )


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: A simple status message.
    """
    logger.debug("Health check called")
    return {"status": "healthy"}


@app.post(
    "/research",
    response_model=ResearchResponse,
    summary="Perform research on a topic",
    description="Performs research on the given topic and returns the results in the specified format."
)
async def do_research(
    request: ResearchRequest = Body(...),
    settings: Settings = Depends(get_settings)
):
    """
    Perform research on a topic.
    
    Args:
        request (ResearchRequest): The research request parameters.
        settings (Settings): Application settings.
        
    Returns:
        ResearchResponse: The research results.
        
    Raises:
        HTTPException: If there's an error in the research process.
    """
    logger.info(f"Received research request - Topic: '{request.topic}', Format: '{request.format}'")
    
    try:
        result = await research_service.perform_research(
            topic=request.topic,
            output_format=request.format
        )
        logger.info(f"Successfully completed research for topic: '{request.topic}'")
        return ResearchResponse(**result)
    except (ResearchError, AgentSessionError, ResearchResponseError):
        # These will be handled by our exception handlers
        raise
    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"Unexpected error in research endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )