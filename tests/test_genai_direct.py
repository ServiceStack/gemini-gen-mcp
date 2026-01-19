import os
import pytest
import time
import signal
import socket
from google import genai
from google.genai import types

# Force IPv4 to avoid macOS hang with broken IPv6
orig_getaddrinfo = socket.getaddrinfo
def patched_getaddrinfo(*args, **kwargs):
    responses = orig_getaddrinfo(*args, **kwargs)
    return [res for res in responses if res[0] == socket.AF_INET]
socket.getaddrinfo = patched_getaddrinfo

def handler(signum, frame):
    raise TimeoutError("Test timed out after 30 seconds")

def get_api_key() -> str:
    """Get Gemini API key from environment."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        pytest.skip("GEMINI_API_KEY environment variable is required")
    return api_key

def test_genai_direct_image_gen():
    """Directly test Gemini image generation using genai.Client."""
    api_key = get_api_key()
    client = genai.Client(api_key=api_key,
        http_options={
            'timeout': 30.0  # 30 seconds timeout
        })
    
    prompt = "A simple red cube on a white background"
    model = "gemini-2.5-flash-image"  # ImageModels.NANO_BANANA
    
    print(f"\nCalling Gemini API for image generation with prompt: '{prompt}'...")
    
    # Set up alarm for timeout
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(30)
    
    try:
        response = client.models.generate_content(
            model=model,
            contents=f"Generate an image: {prompt}",
            config=types.GenerateContentConfig(
                response_modalities=["image"],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1",
                ),
            ),
        )
        # Disable alarm
        signal.alarm(0)
        
        assert response.candidates is not None
        assert len(response.candidates) > 0
        
        parts = response.candidates[0].content.parts
        image_part = next((p for p in parts if hasattr(p, "inline_data") and p.inline_data), None)
        
        assert image_part is not None, "No image part found in response"
        assert image_part.inline_data.data is not None
        assert image_part.inline_data.mime_type.startswith("image/")
        
        mime_type = image_part.inline_data.mime_type
        data = image_part.inline_data.data
        fmt = mime_type.split("/")[1] if "/" in mime_type else "png"
        
        timestamp = int(time.time() * 1000)
        filename = f"test_gen_{timestamp}.{fmt}"
        
        with open(filename, "wb") as f:
            f.write(data)
            
        print(f"Success! Image received and saved to {filename}")
        print(f"Mime type: {mime_type}")
        print(f"Data size: {len(data)} bytes")
        
    except Exception as e:
        pytest.fail(f"Direct Gemini API call failed: {e}")

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-s"])
