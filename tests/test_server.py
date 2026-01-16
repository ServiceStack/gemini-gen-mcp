"""Test suite for gemini-gen-mcp server."""

import pytest
import os
from unittest.mock import patch, MagicMock


def test_get_api_key_missing():
    """Test that get_api_key raises ValueError when GEMINI_API_KEY is not set."""
    from src.gemini_gen_mcp.server import get_api_key
    
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is required"):
            get_api_key()


def test_get_api_key_present():
    """Test that get_api_key returns the API key when set."""
    from src.gemini_gen_mcp.server import get_api_key
    
    test_key = "test-api-key-123"
    with patch.dict(os.environ, {"GEMINI_API_KEY": test_key}):
        assert get_api_key() == test_key


@pytest.mark.asyncio
async def test_text_to_image_validation():
    """Test text_to_image validates num_images parameter."""
    from src.gemini_gen_mcp.server import text_to_image
    
    # Access the underlying function
    func = text_to_image.fn
    
    # Set a fake API key so validation runs
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
        # Test invalid num_images (too low)
        result = await func("test prompt", num_images=0)
        assert "Error: num_images must be between 1 and 4" in result
        
        # Test invalid num_images (too high)
        result = await func("test prompt", num_images=5)
        assert "Error: num_images must be between 1 and 4" in result


@pytest.mark.asyncio
async def test_text_to_image_missing_api_key():
    """Test text_to_image handles missing API key gracefully."""
    from src.gemini_gen_mcp.server import text_to_image
    
    func = text_to_image.fn
    
    with patch.dict(os.environ, {}, clear=True):
        result = await func("test prompt")
        assert "Error generating image:" in result
        assert "GEMINI_API_KEY" in result


@pytest.mark.asyncio
async def test_text_to_audio_missing_api_key():
    """Test text_to_audio handles missing API key gracefully."""
    from src.gemini_gen_mcp.server import text_to_audio
    
    func = text_to_audio.fn
    
    with patch.dict(os.environ, {}, clear=True):
        result = await func("test text")
        assert "Error generating audio:" in result
        assert "GEMINI_API_KEY" in result


@pytest.mark.asyncio
async def test_text_to_image_success_mock():
    """Test text_to_image with mocked successful response."""
    from src.gemini_gen_mcp.server import text_to_image
    
    func = text_to_image.fn
    
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
        with patch("src.gemini_gen_mcp.server.genai.Client") as mock_client:
            # Create mock response structure
            mock_part = MagicMock()
            mock_part.inline_data.data = b"fake_image_data"
            mock_part.inline_data.mime_type = "image/png"
            
            mock_candidate = MagicMock()
            mock_candidate.content.parts = [mock_part]
            
            mock_response = MagicMock()
            mock_response.candidates = [mock_candidate]
            
            mock_instance = MagicMock()
            mock_instance.models.generate_content.return_value = mock_response
            mock_client.return_value = mock_instance
            
            result = await func("a beautiful sunset")
            assert "Error" not in result


@pytest.mark.asyncio
async def test_text_to_audio_success_mock():
    """Test text_to_audio with mocked successful response."""
    from src.gemini_gen_mcp.server import text_to_audio
    
    func = text_to_audio.fn
    
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
        with patch("src.gemini_gen_mcp.server.genai.Client") as mock_client:
            # Create mock response structure
            mock_part = MagicMock()
            mock_part.inline_data.data = b"fake_audio_data"
            mock_part.inline_data.mime_type = "audio/wav"
            
            mock_candidate = MagicMock()
            mock_candidate.content.parts = [mock_part]
            
            mock_response = MagicMock()
            mock_response.candidates = [mock_candidate]
            
            mock_instance = MagicMock()
            mock_instance.models.generate_content.return_value = mock_response
            mock_client.return_value = mock_instance
            
            result = await func("Hello, world!")
            assert "Error" not in result
