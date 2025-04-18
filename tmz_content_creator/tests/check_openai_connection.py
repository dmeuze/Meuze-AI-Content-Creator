import pytest
from unittest.mock import patch, MagicMock
from tmz_content_creator.services.openai_service import OpenAIService

def test_openai_connection():
    """Test that OpenAI service can establish a connection and make a simple request"""
    with patch('tmz_content_creator.services.openai_service.OpenAI') as mock_openai:
        # Setup mock response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Test response"
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        # Initialize service and make request
        service = OpenAIService()
        response = service.generate_content("Test prompt")

        # Verify the response
        assert response == "Test response"
        mock_client.chat.completions.create.assert_called_once()

def test_openai_error_handling():
    """Test that OpenAI service handles errors gracefully"""
    with patch('tmz_content_creator.services.openai_service.OpenAI') as mock_openai:
        # Setup mock to raise an exception
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client

        # Initialize service and make request
        service = OpenAIService()
        response = service.generate_content("Test prompt")

        # Verify error handling
        assert response is None 