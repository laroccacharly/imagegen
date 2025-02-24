import pydantic
from pathlib import Path
import openai
import requests
from dotenv import load_dotenv
load_dotenv()

class ImageGenRequest(pydantic.BaseModel):
    prompt_path: Path = Path("prompt.txt")
    model: str = "dall-e-3"
    size: str = "1024x1024"
    quality: str = "hd"
    style: str = "vivid"  # natural is more natural looking, vivid is more dramatic
    n: int = 1
    output_dir: Path = Path("output")

def get_prompt(request: ImageGenRequest) -> str:    
    with open(request.prompt_path, "r") as f:
        return f.read()
    
def image_name_from_prompt(prompt: str) -> str:
    # Take first few words (up to 4) and join with underscores
    words = prompt.strip().split()[:4]
    prefix = "_".join(words).lower()
    
    # Add length of prompt as suffix
    suffix = str(len(prompt))
    
    # Sanitize filename by removing special characters
    prefix = "".join(c for c in prefix if c.isalnum() or c == '_')
    
    return f"{prefix}_{suffix}.png"

def imagegen(request: ImageGenRequest):
    prompt = get_prompt(request)
    client = openai.OpenAI()
    print("Sending request to OpenAI...")
    response = client.images.generate(
            model=request.model,
            prompt=prompt,
            size=request.size,
            quality=request.quality,
            style=request.style,
            n=request.n,
        )
    print("Received response from OpenAI.")
    url = response.data[0].url
    print(f"Downloading image...")
    response = requests.get(url)
    response.raise_for_status()

    image_name = image_name_from_prompt(prompt)
    image_path = request.output_dir / image_name
    image_path.parent.mkdir(parents=True, exist_ok=True)
    with open(image_path, "wb") as file:
        file.write(response.content)
    print(f"Image downloaded successfully to {image_path}")

if __name__ == "__main__":
    request = ImageGenRequest()
    imagegen(request)
