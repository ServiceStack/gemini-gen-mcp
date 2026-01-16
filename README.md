# Gemini Gen MCP

[![PyPI version](https://badge.fury.io/py/gemini-gen-mcp.svg)](https://badge.fury.io/py/gemini-gen-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MCP Server for Gemini Image and Audio generation using Google's Gemini AI models.

## Features

This MCP server provides tools to:
- **Generate images from text** using Gemini's Flash Image model
- **Generate audio from text** using Gemini 2.5 Flash Preview TTS model

## Installation

### From PyPI

```bash
pip install gemini-gen-mcp
```

### From Source

```bash
git clone https://github.com/ServiceStack/gemini-gen-mcp.git
cd gemini-gen-mcp
pip install -e .
```

## Prerequisites

You need a Google Gemini API key to use this server. Get one from [Google AI Studio](https://aistudio.google.com/apikey).

Set the API key as an environment variable:

```bash
export GEMINI_API_KEY='your-api-key-here'
```

## Usage

### Running the Server

Run the MCP server directly:

```bash
gemini-gen-mcp
```

Or as a Python module:

```bash
python -m gemini_gen_mcp.server
```

### Using with Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gemini-gen": {
      "command": "gemini-gen-mcp",
      "env": {
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Available Tools

#### text_to_image

Generate images from text descriptions.

**Parameters:**
- `prompt` (string, required): Text description of the image to generate
- `model` (string, optional): Gemini model to use (default: "gemini-2.0-flash-exp")
- `num_images` (integer, optional): Number of images to generate, 1-4 (default: 1)

**Example:**
```json
{
  "prompt": "A serene mountain landscape at sunset with a lake",
  "model": "gemini-2.0-flash-exp",
  "num_images": 1
}
```

#### text_to_audio

Generate audio/speech from text.

**Parameters:**
- `text` (string, required): Text to convert to speech
- `model` (string, optional): Gemini model to use (default: "gemini-2.0-flash-exp")
- `voice` (string, optional): Voice to use for speech generation

**Example:**
```json
{
  "text": "Hello, this is a test of the Gemini text to speech system.",
  "model": "gemini-2.0-flash-exp"
}
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/ServiceStack/gemini-gen-mcp.git
cd gemini-gen-mcp

# Install in editable mode with dependencies
pip install -e .
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please use the [GitHub Issues](https://github.com/ServiceStack/gemini-gen-mcp/issues) page.

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Powered by [Google Gemini AI](https://ai.google.dev/)

## Links

- [PyPI Package](https://pypi.org/project/gemini-gen-mcp/)
- [GitHub Repository](https://github.com/ServiceStack/gemini-gen-mcp)
- [Google AI Studio](https://aistudio.google.com/)
- [MCP Documentation](https://modelcontextprotocol.io/)
