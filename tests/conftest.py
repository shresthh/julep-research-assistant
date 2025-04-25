"""
Pytest configuration for testing the Julep Research Assistant.
"""

import pytest
from fastapi.testclient import TestClient

from app.api.endpoints import app
from app.core.agent import JulepAgentManager


# Mock Julep client responses
class MockJulep:
    """Mock Julep client for testing."""
    
    class MockAgents:
        """Mock Agents class."""
        
        def create(self, **kwargs):
            """Mock create method."""
            class MockAgent:
                id = "mock-agent-id"
            
            return MockAgent()
    
    class MockSessions:
        """Mock Sessions class."""
        
        def create(self, **kwargs):
            """Mock create method."""
            class MockSession:
                id = "mock-session-id"
            
            return MockSession()
        
        def chat(self, **kwargs):
            """Mock chat method."""
            class MockResponse:
                class MockChoice:
                    class MockMessage:
                        content = "Mock research result about the requested topic."
                    
                    message = MockMessage()
                
                choices = [MockChoice()]
            
            return MockResponse()
    
    def __init__(self, api_key):
        """Initialize mock Julep client."""
        self.agents = self.MockAgents()
        self.sessions = self.MockSessions()


@pytest.fixture
def mock_julep_agent_manager(monkeypatch):
    """
    Fixture to mock the JulepAgentManager for testing.
    
    Args:
        monkeypatch: Pytest monkeypatch fixture.
        
    Returns:
        JulepAgentManager: A mocked agent manager.
    """
    # Create a mocked agent manager
    agent_manager = JulepAgentManager()
    
    # Replace the Julep client with our mock
    agent_manager.julep = MockJulep(api_key="mock-api-key")
    agent_manager._agent_id = "mock-agent-id"
    
    return agent_manager


@pytest.fixture
def client():
    """
    Fixture to create a TestClient for FastAPI app.
    
    Returns:
        TestClient: A FastAPI TestClient.
    """
    return TestClient(app)