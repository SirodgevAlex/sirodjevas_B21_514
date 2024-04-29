from PIL import Image
import numpy as np

def bernsen_adaptive_binarization(image, r, t, contrast_limit):
    if image.mode != 'L':
        image = image.convert('L')
    
    img_array = np.array(image)
    height, width = img_array.shape
    binary_image = np.zeros((height, width), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            min_val = 255
            max_val = 0
            
            for j in range(max(0, y - r), min(height, y + r + 1)):
                for i in range(max(0, x - r), min(width, x + r + 1)):
                    min_val = min(min_val, img_array[j, i])
                    max_val = max(max_val, img_array[j, i])
            
            avg = np.mean([min_val, max_val])
            contrast = max_val - min_val
            
            if contrast < contrast_limit:
                binary_image[y, x] = 255
            else:
                if img_array[y, x] >= avg * (1 - t):
                    binary_image[y, x] = 255
                else:
                    binary_image[y, x] = 0
            
    return binary_image

image_path = "input/3.png"
image = Image.open(image_path)

r = 5
t = 0.01
contrast_limit = 15

binary_image = bernsen_adaptive_binarization(image, r, t, contrast_limit)

binary_image_path = "output/3.png"
Image.fromarray(binary_image).save(binary_image_path)
