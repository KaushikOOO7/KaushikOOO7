from PIL import Image, ImageEnhance
import cv2
import numpy as np
from rembg import remove
import sys


def prepare_photo(input_path, output_path="source-prepped.png"):
    # Load image
    with open(input_path, "rb") as f:
        input_data = f.read()

    # Remove background
    output_data = remove(input_data)

    # Save temporarily
    with open("temp_no_bg.png", "wb") as f:
        f.write(output_data)

    # Open image
    img = Image.open("temp_no_bg.png").convert("RGBA")

    # Create white background
    background = Image.new("RGBA", img.size, (255, 255, 255, 255))
    background.alpha_composite(img)

    # Convert to RGB
    rgb = background.convert("RGB")

    # Convert PIL image to OpenCV format
    cv_img = np.array(rgb)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)

    # Improve local contrast using CLAHE
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    # Convert back to PIL
    result = Image.fromarray(enhanced)

    # Slight contrast enhancement
    result = ImageEnhance.Contrast(result).enhance(1.15)

    # Save final image
    result.save(output_path)

    print(f"Prepared image saved as: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <photo>")
        sys.exit(1)

    prepare_photo(sys.argv[1])
