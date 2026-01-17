"""MCP Server for Gemini Image and Audio generation using fastmcp."""

import os
import base64
from typing import Optional
from google import genai
from google.genai import types
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("gemini-gen-mcp")


def get_api_key() -> str:
    """Get Gemini API key from environment."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is required. "
            "Get your API key from https://aistudio.google.com/apikey"
        )
    return api_key


@mcp.tool()
async def text_to_image(
    prompt: str,
    model: str = "gemini-2.0-flash-exp",
    num_images: int = 1,
) -> str:
    """Generate images from text using Gemini's Flash Image model.
    
    Args:
        prompt: Text description of the image to generate
        model: Gemini model to use (default: gemini-2.0-flash-exp)
        num_images: Number of images to generate (1-4, default: 1)
    
    Returns:
        Base64 encoded image data with metadata
    """
    try:
        # Configure Gemini API
        client = genai.Client(api_key=get_api_key())
        
        # Validate num_images
        if not 1 <= num_images <= 4:
            return "Error: num_images must be between 1 and 4"
        
        # Generate image with the prompt
        response = client.models.generate_content(
            model=model,
            contents=f"Generate an image: {prompt}",
            config=types.GenerateContentConfig(
                response_modalities=["image"],
            )
        )
        
        # Extract images from response
        images = []
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    # Get image data
                    image_data = part.inline_data.data
                    mime_type = part.inline_data.mime_type
                    
                    # Convert to base64 if not already
                    if isinstance(image_data, bytes):
                        image_b64 = base64.b64encode(image_data).decode('utf-8')
                    else:
                        image_b64 = image_data
                    
                    images.append({
                        "data": image_b64,
                        "mime_type": mime_type
                    })
        
        if not images:
            return "Error: No images were generated"
        
        # Return result
        result = {
            "prompt": prompt,
            "model": model,
            "num_images": len(images),
            "images": images
        }
        
        return str(result)
        
    except Exception as e:
        return f"Error generating image: {str(e)}"


@mcp.tool()
async def text_to_audio(
    text: str,
    model: str = "gemini-2.0-flash-exp",
    voice: Optional[str] = None,
) -> str:
    """Generate audio from text using Gemini Flash TTS model.
    
    Args:
        text: Text to convert to speech
        model: Gemini model to use (default: gemini-2.0-flash-exp)
        voice: Voice to use (optional)
    
    Returns:
        Base64 encoded audio data with metadata
    """
    try:
        # Configure Gemini API
        client = genai.Client(api_key=get_api_key())
        
        # Generate audio with the text
        response = client.models.generate_content(
            model=model,
            contents=f"Read this text: {text}",
            config=types.GenerateContentConfig(
                response_modalities=["audio"],
            )
        )
        
        # Extract audio from response
        audio_data = None
        mime_type = None
        
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    # Get audio data
                    audio_data = part.inline_data.data
                    mime_type = part.inline_data.mime_type
                    break
        
        if not audio_data:
            return "Error: No audio was generated"
        
        # Convert to base64 if not already
        if isinstance(audio_data, bytes):
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')
        else:
            audio_b64 = audio_data
        
        # Return result
        result = {
            "text": text,
            "model": model,
            "voice": voice,
            "audio": {
                "data": audio_b64,
                "mime_type": mime_type
            }
        }
        
        return str(result)
        
    except Exception as e:
        return f"Error generating audio: {str(e)}"


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
