from PIL import Image
from pathlib import Path
import os

def compress_image(input_path: str, output_path: str, target_size_mb: float = 2.0, quality_step: int = 5):
    target_size_bytes = target_size_mb * 1024 * 1024
    
    img = Image.open(input_path)
    
    # Convert to RGB if necessary (removing alpha channel can help reduce size)
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    
    # Start with quality 95
    quality = 95
    
    while quality > 0:
        # Save with current quality
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        # Check file size
        current_size = os.path.getsize(output_path)
        
        if current_size <= target_size_bytes:
            print(f"Successfully compressed image to {current_size / 1024 / 1024:.2f} MB with quality {quality}")
            return True
            
        # Reduce quality for next iteration
        quality -= quality_step
    
    print("Could not compress image to target size even with minimum quality")
    return False

if __name__ == "__main__":
    base_path = Path("family") / "output"
    input_file = base_path / "base.png"
    # Create output filename correctly using Path operations
    output_file = base_path / f"compressed_{input_file.stem}.png"
    compress_image(input_file, output_file, target_size_mb=2.0) 