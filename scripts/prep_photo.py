import sys
import os
import cv2
import numpy as np
from PIL import Image

def prep_photo(input_path, output_path="source-prepped.png"):
    if not os.path.exists(input_path):
        print(f"Error: File {input_path} not found.")
        sys.exit(1)

    print(f"Processing photo: {input_path}")
    
    # 1. Background removal
    try:
        from rembg import remove
        with open(input_path, 'rb') as i:
            input_bytes = i.read()
            output_bytes = remove(input_bytes)
        
        # Load RGBA image
        img_np = np.frombuffer(output_bytes, np.uint8)
        img_rgba = cv2.imdecode(img_np, cv2.IMREAD_UNCHANGED)
    except Exception as e:
        print(f"Warning: rembg failed or not installed ({e}). Falling back to original image.")
        img_bgr = cv2.imread(input_path)
        if img_bgr is None:
            print(f"Error: Could not read image {input_path}")
            sys.exit(1)
        # Create dummy RGBA
        b, g, r = cv2.split(img_bgr)
        alpha = np.ones(b.shape, dtype=b.dtype) * 255
        img_rgba = cv2.merge([b, g, r, alpha])

    # Extract RGB and Alpha
    if img_rgba.shape[2] == 4:
        rgb = img_rgba[:, :, :3]
        alpha = img_rgba[:, :, 3] / 255.0
    else:
        rgb = img_rgba
        alpha = np.ones((rgb.shape[0], rgb.shape[1]), dtype=float)

    # 2. Convert to Grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

    # 3. Apply CLAHE (Contrast-Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(gray)

    # 4. Composite onto pure white background
    white_bg = np.ones_like(enhanced_gray) * 255
    final_img = (enhanced_gray * alpha + white_bg * (1.0 - alpha)).astype(np.uint8)

    # Save output
    cv2.imwrite(output_path, final_img)
    print(f"Saved prepped photo to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prep_photo(sys.argv[1])
    else:
        print("Usage: python scripts/prep_photo.py <source-photo.jpg>")
