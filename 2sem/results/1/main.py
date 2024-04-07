from PIL import Image

def rgb_to_grayscale(image):
    width, height = image.size

    gray_image = Image.new("L", (width, height))

    for y in range(height):
        for x in range(width):
            pixel_value = image.getpixel((x, y))

            if isinstance(pixel_value, int):
                gray_image.putpixel((x, y), pixel_value)
            else:
                brightness = int(0.3 * pixel_value[0] + 0.59 * pixel_value[1] + 0.11 * pixel_value[2])
                gray_image.putpixel((x, y), brightness)

    return gray_image

image = Image.open("example.png")

gray_image = rgb_to_grayscale(image)

gray_image.save("gray_example.png")

gray_image.show()
