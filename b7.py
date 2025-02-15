from PIL import Image
import requests
from io import BytesIO
import base64
import os

def run_b7_1(source: str, output_path: str, width: int, height: int):
    """
    Resize an image from a URL, file path, or base64 string to the specified size.
    
    :param source: URL, file path, or base64 string of the image.
    :param size: Tuple (width, height) for resizing, default is (300, 300).
    :return: Resized PIL Image object.
    """
    try:
        
        # Load image from URL, file, or base64 string
        if source.startswith("http"):  # Check if source is a URL
            response = requests.get(source)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
        elif source.startswith("data:image"):  # Check if source is a base64 string
            base64_data = source.split(",", 1)[1]  # Remove the header
            img = Image.open(BytesIO(base64.b64decode(base64_data)))
        else:
            img = Image.open(source)  # Assume it's a local file
        
        # Resize image
        img_resized = img.resize((width, height), Image.ANTIALIAS)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save the resized image
        img_resized.save(output_path)

        return 'done'
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# Example Usage
# resized_img = resize_image("https://example.com/image.jpg", (200, 200))
# resized_img.show() if resized_img else print("Failed to process image")
