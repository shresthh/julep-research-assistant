"""
Pydantic models for API request and response validation.

This module contains Pydantic models for validating API requests and responses.
"""

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    """
    Model for research request validation.
    """
    topic: str = Field(..., description="The research topic")
    format: str = Field(
        default="summary",
        description="The desired output format (summary, bullet points, short report)"
    )

    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "topic": "artificial intelligence ethics",
                "format": "bullet points"
            }
        }


class ResearchResponse(BaseModel):
    """
    Model for research response validation.
    """
    topic: str = Field(..., description="The research topic")
    format: str = Field(..., description="The output format used")
    result: str = Field(..., description="The research results")

    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "topic": "artificial intelligence ethics",
                "format": "bullet points",
                "result": "• AI ethics concerns the moral implications of AI systems.\n• Key issues include privacy, bias, and accountability.\n• Many organizations have developed ethical guidelines for AI.\n• Ethical AI requires diverse perspectives.\n• Challenges include balancing innovation with safety."
            }
        }