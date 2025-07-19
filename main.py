import argparse
from math import floor
from pathlib import Path
from openai import OpenAI
import base64
from dotenv import load_dotenv
import time 
import uuid
from compress import compress_image
from crop import crop_to_16_9

load_dotenv()

client = OpenAI()

def get_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", "-d", type=str, required=True)
    parser.add_argument("--num_images", "-n", type=int, default=1)
    return parser.parse_args()

def get_dir() -> Path: 
    args = get_args()
    return Path(args.dir)

def get_num_images() -> int: 
    args = get_args()
    return args.num_images

def get_output_dir() -> Path: 
    directory = get_dir()
    output_dir = directory / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir

def load_prompt(): 
    directory = get_dir()
    path = directory / "prompt.txt"
    with open(path, "r") as f:
        return f.read()
    
def load_images(): 
    images = []
    directory = get_dir()
    for file in directory.glob("*.png"):
        if not file.name.startswith("_"):
            images.append(open(file, "rb"))
    if not images:
        raise ValueError(f"No suitable PNG images found in {directory}. Please add at least one image not starting with '_'")
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
        n=get_num_images(),
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

        # Generate a random UUID for this image
        image_uuid = str(uuid.uuid4())[:8]

        # Save the original image
        original_path = get_output_dir() / f"{image_uuid}.png"
        with open(original_path, "wb") as f:
            f.write(image_bytes)
        
        # Compress the image
        compressed_path = get_output_dir() / f"{image_uuid}_compressed.png"
        compress_image(str(original_path), str(compressed_path), target_size_mb=2.0)
        
        # Crop the original image to 16:9
        cropped_path = get_output_dir() / f"{image_uuid}_16_9.png"
        crop_to_16_9(str(original_path), str(cropped_path))

if __name__ == "__main__":
    main()