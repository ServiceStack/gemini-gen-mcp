import pytest
import os
from src.gemini_gen_mcp.server import text_to_image, ImageModels, AspectRatio
from fastmcp.utilities.types import Image

@pytest.mark.asyncio
async def test_text_to_image_integration():
    """Integration test for text_to_image that calls the real API."""
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        pytest.skip("GEMINI_API_KEY not set, skipping integration test")
    
    # We use the function's .fn property because it's wrapped by @mcp.tool()
    func = text_to_image.fn
    
    prompt = "A simple red cube on a white background"
    # use the default model
    model = ImageModels.NANO_BANANA
    
    try:
        result = await func(
            prompt=prompt,
            model=model,
            aspect_ratio=AspectRatio.SQUARE,
        )
        
        assert isinstance(result, Image)
        assert result.data is not None
        assert len(result.data) > 0
        assert result.format in ["png", "jpg", "jpeg"]
        
        print(f"\nIntegration test success! Image generated, size: {len(result.data)} bytes")
        
    except Exception as e:
        pytest.fail(f"Integration test failed with error: {e}")

if __name__ == "__main__":
    # If run directly, run the test with pytest
    import sys
    pytest.main([__file__])
