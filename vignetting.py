import cv2
import numpy as np

def enhance_vignette_and_shrink(image_path, output_path, shrink_intensity=0.6, darkness=1.0):
    # 1. Load the image
    img = cv2.imread(image_path).astype(np.float32)
    if img is None:
        print("Error: Could not find Picture1.jpg")
        return

    h, w = img.shape[:2]
    center_x, center_y = w / 2, h / 2

    # 2. Create a radial distance map
    # This identifies how far each pixel is from the center
    y, x = np.ogrid[:h, :w]
    dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    
    # Normalize distance (0 at center, 1 at the corners)
    max_dist = np.sqrt(center_x**2 + center_y**2)
    dist_norm = dist / max_dist

    # 3. Create the Vignette Mask
    # 'shrink_intensity' controls where the darkness starts (higher = smaller pattern)
    # We use a power function (gamma) to keep the center clear and fade the edges
    vignette = 1.0 - (dist_norm * shrink_intensity)
    vignette = np.clip(vignette, 0, 1)
    
    # Sharpen the gradient transition so it 'eats' the pattern edges
    vignette = np.power(vignette, 2.5 * darkness)

    # 4. Apply the mask
    # Convert vignette to 3 channels (BGR)
    vignette_3d = cv2.merge([vignette, vignette, vignette])
    
    # We multiply the original image by our dark mask
    result = img * vignette_3d

    # 5. Optional: Match the original background gray level
    # Instead of fading to pure black, we fade to the dark gray of your borders
    bg_color = np.array([45, 45, 45]) # Approximate dark gray from Picture1
    final_result = result + (bg_color * (1 - vignette_3d))

    # Save
    cv2.imwrite(output_path, np.clip(final_result, 0, 255).astype(np.uint8))
    print(f"Vignette applied. Pattern minimized.")

# shrink_intensity: 0.1 to 1.5 (Higher = more pattern is hidden)
# darkness: Higher = faster transition to dark background
enhance_vignette_and_shrink('Picture1.jpg', 'vignette_shrunk.jpg', shrink_intensity=1.6, darkness=0.5)