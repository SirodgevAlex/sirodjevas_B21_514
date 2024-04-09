from PIL import Image

def create_difference_image(image1, image2):
    if image1.size != image2.size:
        raise ValueError("Размеры изображений не совпадают")
    
    width, height = image1.size
    difference_image = Image.new("L", (width, height))

    for y in range(height):
        for x in range(width):
            pixel1 = image1.getpixel((x, y))
            pixel2 = image2.getpixel((x, y))
            difference_pixel = abs(pixel1 - pixel2)
            difference_image.putpixel((x, y), difference_pixel)
    
    return difference_image

image_before_filter_path = 'imgs/input/before_filter.png'
image_before_filter = Image.open(image_before_filter_path).convert('L')

image_after_filter_path = 'imgs/input/after_filter.png'
image_after_filter = Image.open(image_after_filter_path).convert('L')

difference_image = create_difference_image(image_before_filter, image_after_filter)

difference_image.show(title='Difference Image')

difference_image.save('imgs/output/difference_image.png')