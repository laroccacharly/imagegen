from pathlib import Path
from PIL import Image

def crop_to_16_9(input_path, output_path):
    """
    Crop the top and bottom of the image equally so that the resulting image is 16:9 aspect ratio.
    Args:
        input_path (str): Path to the input image
        output_path (str): Path where the output image will be saved
    """
    image = Image.open(input_path)
    width, height = image.size
    target_height = int(width * 9 / 16)

    if target_height > height:
        print("Image is already shorter than 16:9 aspect ratio. Cannot crop further.")
        image.save(output_path) # Save the original if no crop needed or possible
        return
    elif target_height == height:
        print("Image is already 16:9 aspect ratio. No crop needed.")
        image.save(output_path) # Save the original if no crop needed
        return

    # Calculate total pixels to remove and how much from top and bottom
    total_pixels_to_remove = height - target_height
    pixels_to_remove_top = total_pixels_to_remove // 2
    pixels_to_remove_bottom = total_pixels_to_remove - pixels_to_remove_top # Accounts for odd numbers

    # Crop equally from the top and bottom
    left = 0
    upper = pixels_to_remove_top
    right = width
    lower = height - pixels_to_remove_bottom
    cropped_image = image.crop((left, upper, right, lower))
    cropped_image.save(output_path)
    print(f"Image cropped equally from top and bottom to 16:9 and saved to {output_path}")

if __name__ == "__main__":
    base_path = Path("polar") / "output"
    input_image = base_path / "base.png"
    output_image = base_path / "base_16_9.png"
    crop_to_16_9(input_image, output_image) 