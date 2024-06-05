import os
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageFont, ImageDraw, ImageOps

PHRASE = "жүрегіңді көрсең де, жүректерді көрмесең де, олар бар"
WHITE = 255

FONT_SIZE = 52
SPACE_LEN = 10
THRESHOLD = 75
FONT_PATH = "input/Times.ttf"
OUTPUT_FOLDER = "output"

FONT = ImageFont.truetype("input/Arial.ttf", 52)
os.makedirs(os.path.join(OUTPUT_FOLDER, "phrase_profile"), exist_ok=True)


def create_phrase_profiles(img: np.array):
    img_b = img != WHITE

    horizontal_profile = np.sum(img_b, axis=0)
    plt.bar(
        x=np.arange(start=1, stop=img_b.shape[1] + 1).astype(int),
        height=horizontal_profile,
        width=0.9
    )
    plt.savefig(os.path.join(OUTPUT_FOLDER, "phrase_profile", "horizontal_profile.png"))
    plt.clf()

    vertical_profile = np.sum(img_b, axis=1)
    plt.barh(
        y=np.arange(start=1, stop=img_b.shape[0] + 1).astype(int),
        width=vertical_profile,
        height=0.9
    )
    plt.savefig(os.path.join(OUTPUT_FOLDER, "phrase_profile", "vertical_profile.png"))
    plt.clf()


def simple_binarization(img, threshold=THRESHOLD):
    binarized_img = np.zeros_like(img)
    binarized_img[img > threshold] = WHITE
    return binarized_img.astype(np.uint8)

def generate_phrase_image():
    space_len = 5
    phrase_width = 0
    max_height = 0

    for char in PHRASE:
        mask = FONT.getmask(char)
        if mask:
            width = mask.getbbox()[2]
            height = mask.getbbox()[3]
            phrase_width += width
            if height > max_height:
                max_height = height

    phrase_width += space_len * (len(PHRASE) - 1)

    img = Image.new("L", (phrase_width, max_height + 40), color="white")
    draw = ImageDraw.Draw(img)

    current_x = 0
    baseline = 0
    for char in PHRASE:
        mask = FONT.getmask(char)
        if mask:
            width = mask.getbbox()[2]
            height = mask.getbbox()[3]
            draw.text((current_x, baseline - height + 30), char, "black", font=FONT)
            current_x += width + space_len

    img = Image.fromarray(simple_binarization(np.array(img)))
    img.save("output/original_phrase.bmp")

    np_img = np.array(img)
    create_phrase_profiles(np_img)
    ImageOps.invert(img).save("output/inverted_phrase.bmp")
    return np_img


def segment_letters(img):
    profile = np.sum(img == 0, axis=0)
    letter_bounds = []

    in_letter = False
    for i, count in enumerate(profile):
        if count > 0:
            if not in_letter:
                start = i
                in_letter = True
        else:
            if in_letter:
                end = i
                in_letter = False
                letter_bounds.append((start - 1, end))

    if in_letter:
        letter_bounds.append((start, len(profile)))

    return letter_bounds


def draw_bounding_boxes(img, bounds):
    image = Image.fromarray(img)
    draw = ImageDraw.Draw(image)

    for start, end in bounds:
        left, right = start, end
        top, bottom = 0, img.shape[0]
        draw.rectangle([left, top, right, bottom], outline="red")

    image.save(os.path.join(OUTPUT_FOLDER, "segmented_phrase.bmp"))


if __name__ == "__main__":
    generated_img = generate_phrase_image()
    letter_bounds = segment_letters(generated_img)
    draw_bounding_boxes(generated_img, letter_bounds)
