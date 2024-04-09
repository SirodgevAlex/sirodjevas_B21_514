from PIL import Image
import numpy as np


def resize(pixels, k):
    new_size = k

    new_pixels = np.zeros((int(new_size * pixels.shape[0]), int(new_size * pixels.shape[1]), 4), dtype=np.uint8)

    for x in range(0, int(pixels.shape[0] * new_size) - 1):
        for y in range(0, int(pixels.shape[1] * new_size) - 1):
            new_pixels[x, y] = np.array(pixels[int(x / new_size), int(y / new_size)])

    return new_pixels

def interpolation(pixels, m):
    return resize(pixels, m / 1)

def decimation(pixels, n):
    return resize(pixels, 1 / n)

def interpolation_decimation(pixels, m, n):
    return decimation(interpolation(pixels, m), n)

def task1():
    img_path = 'lab_1_imgs/im.png'
    img = Image.open(img_path)
    pixels = np.array(img, dtype=np.uint8)

    image = Image.fromarray(interpolation(pixels, 2))
    image.save("lab_1_imgs/im1.png")

def task2():
    img_path = 'lab_1_imgs/im.png'
    img = Image.open(img_path)
    pixels = np.array(img, dtype=np.uint8)

    image = Image.fromarray(decimation(pixels, 2))
    image.save("lab_1_imgs/im2.png")

def task3():
    img_path = 'lab_1_imgs/im.png'
    img = Image.open(img_path)
    pixels = np.array(img, dtype=np.uint8)

    image = Image.fromarray(interpolation_decimation(pixels, 1, 2))
    image.save("lab_1_imgs/im3.png")

def task4():
    img_path = 'lab_1_imgs/im.png'
    img = Image.open(img_path)
    pixels = np.array(img, dtype=np.uint8)

    image = Image.fromarray(resize(pixels, 2))
    image.save("lab_1_imgs/im4.png")

def main():
    task1()
    print("Task 1 suc")
    task2()
    print("Task 2 suc")
    task3()
    print("Task 3 suc")
    task4()
    print("Task 4 suc")



if __name__ == "__main__":
    main()