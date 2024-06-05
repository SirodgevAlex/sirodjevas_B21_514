import csv
import math
import numpy as np
from PIL import Image

KAZAKH_LETTERS_UNICODE = ["0430", "0431", "0432", "0433", "0434", "0435", "0436", "0437", "0438", "0439",
                          "043A", "043B", "043C", "043D", "043E", "043F", "0440", "0441", "0442", "0443",
                          "0444", "0445", "0446", "0447", "0448", "0449", "044A", "044B", "044C", "044D", 
                          "044E", "044F", "04B0", "04B1", "04D9", "049B", "0493", "049B",
                          "04A3", "04AF", "04BB", "04E9"]
KAZAKH_LETTERS = [chr(int(letter, 16)) for letter in KAZAKH_LETTERS_UNICODE]

WHITE = 255
PHRASE = "жүрегіңді көрсең де, жүректерді көрмесең де, олар бар".replace(" ", "")


def calculate_features(img: np.array):
    img_b = np.zeros(img.shape, dtype=int)
    img_b[img != WHITE] = 1

    weight = np.sum(img_b)

    y_indices, x_indices = np.indices(img_b.shape)
    y_center_of_mass = np.sum(y_indices * img_b) / weight
    x_center_of_mass = np.sum(x_indices * img_b) / weight

    inertia_x = np.sum((y_indices - y_center_of_mass) ** 2 * img_b) / weight
    inertia_y = np.sum((x_indices - x_center_of_mass) ** 2 * img_b) / weight

    return weight, x_center_of_mass, y_center_of_mass, inertia_x, inertia_y


def segment_letters(img):
    profile = np.sum(img == 0, axis=0)

    in_letter = False
    letter_bounds = []

    for i in range(len(profile)):
        if profile[i] > 0:
            if not in_letter:
                in_letter = True
                start = i
        else:
            if in_letter:
                in_letter = False
                end = i
                letter_bounds.append((start - 1, end))

    if in_letter:
        letter_bounds.append((start, len(profile)))

    return letter_bounds


def get_alphabet_info() -> dict[chr, tuple]:
    def parse_tuple(string):
        return tuple(map(float, string.strip('()').split(',')))

    tuples_list = dict()
    with open('input/data.csv', 'r') as file:
        reader = csv.DictReader(file)
        i = 0
        for row in reader:
            weight = float(row['weight'])
            center_of_mass = parse_tuple(row['center_of_mass'])
            inertia = parse_tuple(row['inertia'])
            print(weight, center_of_mass, inertia)
            tuples_list[KAZAKH_LETTERS[i]] = weight, *center_of_mass, *inertia
            i += 1
    return tuples_list


def create_hypothesis(alphabet_info: dict[chr, tuple], target_features):
    def euclidean_distance(feature1, feature2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(feature1, feature2)))

    distances = dict()
    for letter, features in alphabet_info.items():
        distance = euclidean_distance(target_features, features)
        distances[letter] = distance

    max_distance = max(distances.values())

    similarities = [(letter, round(1 - distance / max_distance, 2)) for letter, distance in distances.items()]

    return sorted(similarities, key=lambda x: x[1])


def get_phrase_from_hypothesis(img: np.array, bounds) -> str:
    alphabet_info = get_alphabet_info()
    res = []
    for start, end in bounds:
        letter_features = calculate_features(img[:, start: end])
        hypothesis = create_hypothesis(alphabet_info, letter_features)
        best_hypotheses = hypothesis[-1][0]
        res.append(best_hypotheses)
    return "".join(res)


def write_res(recognized_phrase: str):
    max_len = max(len(PHRASE), len(recognized_phrase))
    orig = PHRASE.ljust(max_len)
    detected = recognized_phrase.ljust(max_len)

    with open("output/result.txt", 'w') as f:
        correct_letters = 0
        by_letter = ["has | got | correct"]
        for i in range(max_len):
            is_correct = orig[i] == detected[i]
            by_letter.append(f"{orig[i]}\t{detected[i]}\t{is_correct}")
            correct_letters += int(is_correct)
        f.write("\n".join([
            f"phrase:      {orig}",
            f"detected:    {detected}",
            f"correct:     {math.ceil(correct_letters / max_len * 100)}%\n\n"
        ]))
        f.write("\n".join(by_letter))


if __name__ == "__main__":
    """ 7 Лабораторная работа """
    img = np.array(Image.open(f'input/original_phrase.bmp').convert('L'))
    bounds = segment_letters(img)
    recognized_phrase = get_phrase_from_hypothesis(img, bounds)
    write_res(recognized_phrase)