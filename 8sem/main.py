import os
import typing

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from tqdm import tqdm

WHITE = 255
Point_type = typing.Tuple[int, int]
D = 2
PHI = [angle / 180 * np.pi for angle in [45, 135, 225, 315]]


def analyze_pixel_neighbors(img: Image, pix, pos: Point_type):
    res = np.zeros(WHITE + 1)
    base_x, base_y = pos
    for angle in PHI:
        x = base_x + np.around(np.cos(angle)) * D
        y = base_y + np.around(np.sin(angle)) * D
        if 0 <= x < img.size[0] and 0 <= y < img.size[1]:
            val = pix[x, y]
            res[val] += 1
    return pix[base_x, base_y], res


def pixel_gen(img: Image, func=lambda img, pix, x: pix[x]):
    pix = img.load()
    for row in range(img.size[1]):
        for col in range(img.size[0]):
            pos = (col, row)
            yield pos, func(img, pix, pos)


def create_haralic_matrix_and_stats(name: str, img: Image):
    res = np.zeros((WHITE + 1, WHITE + 1))
    hist = np.zeros(WHITE + 1)
    total_pixels = img.size[0] * img.size[1]
    for pos, (val, row) in tqdm(pixel_gen(img, func=analyze_pixel_neighbors), total=total_pixels):
        res[val] += row
        hist[val] += 1
    max_max = np.max(res)
    res_img = Image.fromarray(np.uint8(res * WHITE / max_max))
    res_img.save(f"{name}_matrix.jpg", "JPEG")

    create_bar(hist, name)
    calc_params(res_img, name)


def calc_params(h_img: Image, filename):
    res_s = pd.Series({"con": 0, "lun": 0})
    for (i, j), p in tqdm(pixel_gen(h_img), total=h_img.size[0] * h_img.size[1]):
        tmp = (i - j) ** 2
        res_s["con"] += tmp * p
        res_s["lun"] += p / (1 + tmp)
    res_s.to_csv(f"{filename}.csv")


def linear_transform(img: Image, a=1, b=0):
    res_img = img.copy()
    d = ImageDraw.Draw(res_img)
    for pos, pixel in pixel_gen(img):
        p = min(int(a * pixel + b), WHITE)
        d.point(pos, p)
    return res_img


def create_bar(hist, img_name):
    plt.figure()
    plt.bar(np.arange(hist.size), hist)
    plt.savefig(f"{img_name}_bar.png")
    plt.close()


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, 'input')
    for image in os.scandir(input_path):
        print(f"Работаем с {image.name}.")
        output_path = os.path.join(current_dir, 'output', image.name.split('.')[0])
        os.makedirs(output_path, exist_ok=True)
        mono_name = os.path.join(output_path, "mono")
        linear_name = os.path.join(output_path, "linear")

        mono_img = Image.open(image.path).convert('L')
        mono_img.save(f"{mono_name}.jpg", "JPEG")

        create_haralic_matrix_and_stats(mono_name, mono_img)

        linear_img = linear_transform(mono_img)
        linear_img.save(f"{linear_name}.jpg", "JPEG")
        create_haralic_matrix_and_stats(linear_name, linear_img)


if __name__ == "__main__":
    main()
