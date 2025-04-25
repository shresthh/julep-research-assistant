"""
Tests for the API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.api.endpoints import app
from app.services.research import research_service


def test_health_check(client):
    """
    Test the health check endpoint.
    
    Args:
        client: TestClient fixture.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_research_endpoint(client, monkeypatch):
    """
    Test the research endpoint.
    
    Args:
        client: TestClient fixture.
        monkeypatch: Pytest monkeypatch fixture.
    """
    # Mock the perform_research method
    async def mock_perform_research(topic, output_format):
        return {
            "topic": topic,
            "format": output_format,
            "result": f"Mock research result about {topic} in {output_format} format."
        }
    
    monkeypatch.setattr(research_service, "perform_research", mock_perform_research)
    
    # Test with valid input
    response = client.post(
        "/research",
        json={"topic": "artificial intelligence", "format": "bullet points"}
    )
    
    assert response.status_code == 200
    assert "topic" in response.json()
    assert "format" in response.json()
    assert "result" in response.json()
    assert response.json()["topic"] == "artificial intelligence"
    assert response.json()["format"] == "bullet points"
    assert "Mock research result" in response.json()["result"]


def test_research_endpoint_default_format(client, monkeypatch):
    """
    Test the research endpoint with default format.
    
    Args:
        client: TestClient fixture.
        monkeypatch: Pytest monkeypatch fixture.
    """
    # Mock the perform_research method
    async def mock_perform_research(topic, output_format):
        return {
            "topic": topic,
            "format": output_format,
            "result": f"Mock research result about {topic} in {output_format} format."
        }
    
    monkeypatch.setattr(research_service, "perform_research", mock_perform_research)
    
    # Test with only topic provided (should use default format)
    response = client.post(
        "/research",
        json={"topic": "climate change"}
    )
    
    assert response.status_code == 200
    assert response.json()["topic"] == "climate change"
    assert response.json()["format"] == "summary"  # Default format
    assert "Mock research result" in response.json()["result"]


def test_research_endpoint_error_handling(client, monkeypatch):
    """
    Test error handling in the research endpoint.
    
    Args:
        client: TestClient fixture.
        monkeypatch: Pytest monkeypatch fixture.
    """
    # Mock the perform_research method to raise an exception
    async def mock_perform_research_error(topic, output_format):
        raise Exception("Test error message")
    
    monkeypatch.setattr(research_service, "perform_research", mock_perform_research_error)
    
    # Test with valid input but service error
    response = client.post(
        "/research",
        json={"topic": "artificial intelligence", "format": "bullet points"}
    )
    
    assert response.status_code == 500
    assert "detail" in response.json()
    assert "Test error message" in response.json()["detail"]