"""
Tests for the Julep agent manager.
"""

import pytest

from app.core.agent import JulepAgentManager


def test_agent_creation(mock_julep_agent_manager):
    """
    Test that the agent can be created successfully.
    
    Args:
        mock_julep_agent_manager: The mocked agent manager.
    """
    # Call create_research_agent method
    agent = mock_julep_agent_manager.create_research_agent()
    
    # Check that the agent was created with an ID
    assert hasattr(agent, 'id')
    assert agent.id == "mock-agent-id"


def test_session_creation(mock_julep_agent_manager):
    """
    Test that a session can be created successfully.
    
    Args:
        mock_julep_agent_manager: The mocked agent manager.
    """
    # Create a session
    situation = "User wants to research about 'AI' and receive results in 'summary' format."
    session = mock_julep_agent_manager.create_session(situation=situation)
    
    # Check that the session was created with an ID
    assert hasattr(session, 'id')
    assert session.id == "mock-session-id"


def test_chat(mock_julep_agent_manager):
    """
    Test that chat works successfully.
    
    Args:
        mock_julep_agent_manager: The mocked agent manager.
    """
    # Create a session first
    situation = "User wants to research about 'AI' and receive results in 'summary' format."
    session = mock_julep_agent_manager.create_session(situation=situation)
    
    # Send a message
    messages = [{"role": "user", "content": "Please research the topic 'AI' and provide the information in 'summary' format."}]
    response = mock_julep_agent_manager.chat(session.id, messages)
    
    # Check the response
    assert hasattr(response, 'choices')
    assert len(response.choices) > 0
    assert hasattr(response.choices[0], 'message')
    assert hasattr(response.choices[0].message, 'content')
    assert isinstance(response.choices[0].message.content, str)
    assert response.choices[0].message.content == "Mock research result about the requested topic."