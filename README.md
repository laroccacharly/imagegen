# Image Generator

A Python-based image generation tool that uses OpenAI's DALL-E 3 API to generate images from text prompts.

## Features

- Generate images using DALL-E 3
- Customizable image parameters (size, quality, style)
- Automatic file naming based on prompt content
- Organized output directory structure

## Installation

1. Clone this repository
2. Create a `.env` file in the project root and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

3. Create a `prompt.txt` file with your image generation prompt
4. Run the script:
```bash
uv run imagegen.py
```

### Configuration

You can customize the image generation by modifying the parameters in `ImageGenRequest`:

- `prompt_path`: Path to the prompt file (default: "prompt.txt")
- `model`: Model to use (default: "dall-e-3")
- `size`: Image size (default: "1024x1024")
- `quality`: Image quality (default: "hd")
- `style`: Generation style - "vivid" or "natural" (default: "vivid")
- `n`: Number of images to generate (default: 1)
- `output_dir`: Directory for generated images (default: "output")

## Output

Generated images are saved in the `output` directory. File names are automatically generated based on the first few words of the prompt and its length.
