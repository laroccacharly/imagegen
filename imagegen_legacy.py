import pydantic
from pathlib import Path
import openai
import httpx
import asyncio
import aiofiles
from dotenv import load_dotenv
load_dotenv()

class ImageGenRequest(pydantic.BaseModel):
    prompt_path: Path = Path("prompt.txt")
    model: str = "dall-e-3"
    size: str = "1024x1024"
    quality: str = "hd"
    style: str = "natural"  # natural is more natural looking, vivid is more dramatic
    n: int = 1
    output_dir: Path = Path("output")

def get_prompt(request: ImageGenRequest) -> str:    
    with open(request.prompt_path, "r") as f:
        return f.read()
    
def image_name_from_prompt(prompt: str, run_index: int) -> str:
    # Take first few words (up to 4) and join with underscores
    words = prompt.strip().split()[:4]
    prefix = "_".join(words).lower()
    
    # Add length of prompt as suffix
    suffix = str(len(prompt))
    
    # Sanitize filename by removing special characters
    prefix = "".join(c for c in prefix if c.isalnum() or c == '_')
    
    return f"{prefix}_{suffix}_{run_index+1}.png"

async def imagegen(request: ImageGenRequest, run_index: int):
    print(f"[Run {run_index+1}] Starting image generation...")
    prompt = get_prompt(request)
    # Use AsyncOpenAI client
    client = openai.AsyncOpenAI()
    print(f"[Run {run_index+1}] Sending request to OpenAI...")
    try:
        response = await client.images.generate(
            model=request.model,
            prompt=prompt,
            size=request.size,
            quality=request.quality,
            style=request.style,
            n=request.n,
        )
    except Exception as e:
        print(f"[Run {run_index+1}] Error during OpenAI request: {e}")
        return
    print(f"[Run {run_index+1}] Received response from OpenAI.")
    url = response.data[0].url
    print(f"[Run {run_index+1}] Downloading image...")
    # Use httpx for async download
    async with httpx.AsyncClient() as http_client:
        img_response = await http_client.get(url)
        img_response.raise_for_status()

    image_name = image_name_from_prompt(prompt, run_index)
    image_path = request.output_dir / image_name
    image_path.parent.mkdir(parents=True, exist_ok=True)
    # Use aiofiles for async file writing
    async with aiofiles.open(image_path, "wb") as file:
        await file.write(img_response.content)
    print(f"[Run {run_index+1}] Image downloaded successfully to {image_path}")

if __name__ == "__main__":
    image_count = 3
    async def main():
        request = ImageGenRequest()
        tasks = [imagegen(request, i) for i in range(image_count)]
        await asyncio.gather(*tasks)

    asyncio.run(main())
