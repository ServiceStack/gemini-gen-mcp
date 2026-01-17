"""Test suite for gemini-gen-mcp server."""

import pytest
import os
from unittest.mock import patch, MagicMock


def test_get_api_key_missing():
    """Test that get_api_key raises ValueError when GEMINI_API_KEY is not set."""
    from src.gemini_gen_mcp.server import get_api_key

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(
            ValueError, match="GEMINI_API_KEY environment variable is required"
        ):
            get_api_key()


def test_get_api_key_present():
    """Test that get_api_key returns the API key when set."""
    from src.gemini_gen_mcp.server import get_api_key

    test_key = "test-api-key-123"
    with patch.dict(os.environ, {"GEMINI_API_KEY": test_key}):
        assert get_api_key() == test_key


@pytest.mark.asyncio
async def test_text_to_image_missing_api_key():
    """Test text_to_image raises ValueError when API key is missing."""
    from src.gemini_gen_mcp.server import text_to_image

    func = text_to_image.fn

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GEMINI_API_KEY"):
            await func("test prompt")


@pytest.mark.asyncio
async def test_text_to_audio_missing_api_key():
    """Test text_to_audio raises ValueError when API key is missing."""
    from src.gemini_gen_mcp.server import text_to_audio

    func = text_to_audio.fn

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GEMINI_API_KEY"):
            await func("test text")


@pytest.mark.asyncio
async def test_text_to_image_success_mock():
    """Test text_to_image with mocked successful response."""
    from src.gemini_gen_mcp.server import text_to_image
    from fastmcp.utilities.types import Image

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
            assert isinstance(result, Image)
            assert result.data == b"fake_image_data"


@pytest.mark.asyncio
async def test_text_to_audio_success_mock():
    """Test text_to_audio with mocked successful response."""
    from src.gemini_gen_mcp.server import text_to_audio
    from fastmcp.utilities.types import Audio

    func = text_to_audio.fn

    # Create valid PCM data (silence) for WAV conversion
    pcm_data = b"\x00\x00" * 24000  # 1 second of silence at 24kHz

    with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
        with patch("src.gemini_gen_mcp.server.genai.Client") as mock_client:
            # Create mock response structure
            mock_part = MagicMock()
            mock_part.inline_data.data = pcm_data
            mock_part.inline_data.mime_type = "audio/L16;codec=pcm;rate=24000"

            mock_candidate = MagicMock()
            mock_candidate.content.parts = [mock_part]

            mock_response = MagicMock()
            mock_response.candidates = [mock_candidate]

            mock_instance = MagicMock()
            mock_instance.models.generate_content.return_value = mock_response
            mock_client.return_value = mock_instance

            result = await func("Hello, world!")
            assert isinstance(result, Audio)
            # WAV header starts with RIFF
            assert result.data[:4] == b"RIFF"


def test_get_download_path():
    """Test get_download_path returns correct path and creates directory."""
    import tempfile
    from src.gemini_gen_mcp.server import get_download_path

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.dict(os.environ, {"GEMINI_DOWNLOAD_PATH": tmpdir}):
            result = get_download_path("test_subdir")
            expected = os.path.join(tmpdir, "test_subdir")
            assert result == expected
            assert os.path.isdir(result)
