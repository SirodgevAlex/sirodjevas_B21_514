from PIL import Image

def median_filter_decision_rule(aperture):
    count_ones = sum(1 for pixel in aperture if pixel > 128)
    count_zeros = sum(1 for pixel in aperture if pixel == 0)
    if count_ones > len(aperture) / 2:
        return 255
    else:
        return 0
    
def median_filter_decision_rule_hill(aperture):
    center_pixel = aperture[len(aperture) // 2]
    neighbor_pixels = [pixel for pixel in aperture if pixel != center_pixel]
    
    if neighbor_pixels:
        if center_pixel > min(neighbor_pixels) and center_pixel < max(neighbor_pixels):
            return center_pixel
        else:
            return max(neighbor_pixels)
    else:
        return center_pixel

def median_filter_decision_rule_valley(aperture):
    center_pixel = aperture[len(aperture) // 2]
    neighbor_pixels = [pixel for pixel in aperture if pixel != center_pixel]
    
    if neighbor_pixels:
        if center_pixel < min(neighbor_pixels) and center_pixel > max(neighbor_pixels):
            return center_pixel
        else:
            return min(neighbor_pixels)
    else:
        return center_pixel

def apply_median_filter(image, filter_size):
    filtered_image = image.copy()
    width, height = image.size
    padding = filter_size // 2
    
    for i in range(padding, width - padding):
        for j in range(padding, height - padding):
            aperture = [image.getpixel((x, y)) for x in range(i - padding, i + padding + 1)
                                                  for y in range(j - padding, j + padding + 1)]
            filtered_image.putpixel((i, j), median_filter_decision_rule_hill(aperture))
    
    return filtered_image

image_path = 'input/1.png'
image = Image.open(image_path).convert('L')

filtered_image = apply_median_filter(image, filter_size=9)

image.show(title='Original Image')
filtered_image.show(title='Filtered Image')

filtered_image.save('output/hill/1.png')
