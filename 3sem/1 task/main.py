from PIL import Image

def median_filter_decision_rule(aperture):
    count_ones = sum(1 for pixel in aperture if pixel > 128)
    count_zeros = sum(1 for pixel in aperture if pixel == 0)
    if count_ones > len(aperture) / 2:
        return 255
    else:
        return 0

def apply_median_filter(image, filter_size):
    filtered_image = image.copy()
    width, height = image.size
    padding = filter_size // 2
    
    for i in range(padding, width - padding):
        for j in range(padding, height - padding):
            print(image.getpixel((i, j)))
            aperture = [image.getpixel((x, y)) for x in range(i - padding, i + padding + 1)
                                                  for y in range(j - padding, j + padding + 1)]
            filtered_image.putpixel((i, j), median_filter_decision_rule(aperture))
    
    return filtered_image

image_path = 'imgs/input/im.png'
image = Image.open(image_path).convert('L')

filtered_image = apply_median_filter(image, filter_size=9)

image.show(title='Original Image')
filtered_image.show(title='Filtered Image')

filtered_image.save('imgs/output/filtered_image.png')