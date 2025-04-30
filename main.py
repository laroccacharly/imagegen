from math import floor
from pathlib import Path
from openai import OpenAI
import base64
from dotenv import load_dotenv
import time 
load_dotenv()

client = OpenAI()
image_name = "polar"
DIRECTORY = Path(image_name) # where the prompt and images are
OUTPUT_DIR = DIRECTORY / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_prompt(): 
    path = DIRECTORY / "prompt.txt"
    with open(path, "r") as f:
        return f.read()
    
def load_images(): 
    images = []
    for file in DIRECTORY.glob("*.png"):
        if not file.name.startswith("_"):
            images.append(open(file, "rb"))
    if not images:
        raise ValueError(f"No suitable PNG images found in {DIRECTORY}. Please add at least one image not starting with '_'")
    return images

def main(): 
    prompt = load_prompt()
    images = load_images()
    start_time = time.time()
    result = client.images.edit( # or client.images.generate
        model="gpt-image-1",
        prompt=prompt,
        image=images,
        size="1536x1024",
        # background="opaque", # opaque, transparent, auto
        n=1,
        # output_format="png",
        quality="medium", # low, medium, high
    )
    end_time = time.time()
    delay = floor(end_time - start_time)
    print(f"Time taken: {delay} seconds")
    data_list = result.data
    print(f"Received {len(data_list)} images")
    for i, data in enumerate(data_list):
        image_base64 = data.b64_json
        image_bytes = base64.b64decode(image_base64)

        with open(OUTPUT_DIR / f"{image_name}_{i}.png", "wb") as f:
            f.write(image_bytes)


if __name__ == "__main__":
    main()