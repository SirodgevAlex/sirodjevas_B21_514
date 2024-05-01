from PIL import Image, ImageDraw, ImageFont
import os

def generate_symbol_image(symbol, font_name, font_size, output_dir):
    font = ImageFont.truetype(font_name, font_size)
    mask = font.getmask(symbol)
    text_width, text_height = mask.size

    top_padding = 0
    bottom_padding = 10
    text_height += top_padding + 5 * bottom_padding
    
    image = Image.new("L", (text_width, text_height), color="white")
    draw = ImageDraw.Draw(image)
    draw.text((0, top_padding), symbol, fill="black", font=font)
    
    output_path = os.path.join(output_dir, f"{symbol}.png")
    image.save(output_path)

def calculate_black_mass(image):
    pixels = list(image.getdata())
    total_pixels = len(pixels)
    black_pixels = sum(1 for pixel in pixels if pixel == 0)
    black_mass = black_pixels / total_pixels
    return black_mass

def calculate_normalized_center(center_x, center_y, image_width, image_height):
    normalized_center_x = center_x / image_width
    normalized_center_y = center_y / image_height
    return normalized_center_x, normalized_center_y

def calculate_moments_of_inertia(image, center_x, center_y):
    width, height = image.size
    pixels = list(image.getdata())
    horizontal_moment = 0
    vertical_moment = 0
    
    for y in range(height):
        for x in range(width):
            pixel = pixels[y * width + x]
            if pixel == 0: 
                horizontal_moment += (y - center_y) ** 2
                vertical_moment += (x - center_x) ** 2
    
    return horizontal_moment, vertical_moment

def calculate_normalized_moments(horizontal_moment, vertical_moment, image_area):
    normalized_horizontal_moment = horizontal_moment / image_area
    normalized_vertical_moment = vertical_moment / image_area
    return normalized_horizontal_moment, normalized_vertical_moment

def calculate_profiles(image):
    width, height = image.size
    pixels = list(image.getdata())
    x_profile = [0] * width
    y_profile = [0] * height
    
    for y in range(height):
        for x in range(width):
            pixel = pixels[y * width + x]
            if pixel == 0:
                x_profile[x] += 1
                y_profile[y] += 1
    
    return x_profile, y_profile

def calculate_center_of_mass(image):
    width, height = image.size
    pixels = list(image.getdata())
    total_pixels = len(pixels)
    total_x = 0
    total_y = 0

    for y in range(height):
        for x in range(width):
            pixel = pixels[y * width + x]
            if pixel == 0:
                total_x += x
                total_y += y
    
    center_x = total_x / total_pixels
    center_y = total_y / total_pixels
    
    return center_x, center_y

def main():
    font_name = "Arial.ttf"
    font_size = 100
    
    output_dir = "symbols"
    os.makedirs(output_dir, exist_ok=True)
    
    symbols = "абвгғдеёжзийкқлмнңоөпрстуұүфхһцчшщъыіьэюя"
    
    for symbol in symbols:
        generate_symbol_image(symbol, font_name, font_size, output_dir)
        
        image = Image.open(os.path.join(output_dir, f"{symbol}.png"))
        
        black_mass = calculate_black_mass(image)
        
        center_x, center_y = calculate_center_of_mass(image)
        
        image_width, image_height = image.size
        normalized_center_x, normalized_center_y = calculate_normalized_center(center_x, center_y, image_width, image_height)
        
        horizontal_moment, vertical_moment = calculate_moments_of_inertia(image, center_x, center_y)
        
        image_area = image_width * image_height
        normalized_horizontal_moment, normalized_vertical_moment = calculate_normalized_moments(horizontal_moment, vertical_moment, image_area)
        
        x_profile, y_profile = calculate_profiles(image)
        
        print(f"Symbol: {symbol}")
        print("Black Mass:", black_mass)
        print("Normalized Center:", (normalized_center_x, normalized_center_y))
        print("Horizontal Moment of Inertia:", horizontal_moment)
        print("Vertical Moment of Inertia:", vertical_moment)
        print("Normalized Horizontal Moment of Inertia:", normalized_horizontal_moment)
        print("Normalized Vertical Moment of Inertia:", normalized_vertical_moment)
        print("X Profile:", x_profile)
        print("Y Profile:", y_profile)
        print()
    
if __name__ == "__main__":
    main()
