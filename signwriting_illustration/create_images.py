import os

import numpy as np
from PIL import Image
import cv2
from tqdm import tqdm

size = 512


def crop_whitespace(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255 * (gray < 128).astype(np.uint8)  # To invert the text to white
    coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
    return img[y:y + h, x:x + w]


def wrap_img(img):
    h, w, _ = img.shape

    f_img = np.full(shape=(size, size, 3), fill_value=255)
    y_offset = (size - h) // 2
    x_offset = (size - w) // 2
    f_img[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img

    return f_img


def downscale(img):
    old_size = img.size

    ratio = size / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])

    return img.resize(new_size, Image.BICUBIC)


os.makedirs("train_A", exist_ok=True)
os.makedirs("train_B", exist_ok=True)

illustrations = sorted([f[:-len(".pdf")] for f in os.listdir('data/Vokabeltrainer/illustrations')])
signwritings = sorted([f[:-len(".png")] for f in os.listdir('glossen') if f.endswith(".png")])

overlap = set(illustrations).intersection(set(signwritings))

print("Found", len(overlap))
print("Illustrations not found", len(illustrations) - len(overlap))
print("Signs not found", len(signwritings) - len(overlap))

overlap = sorted(overlap)

for sign_id in tqdm(overlap):
    # SignWriting
    img = cv2.imread('glossen/' + sign_id + '.png')
    wrapped = wrap_img(crop_whitespace(img))[:, :, :1]
    assert wrapped.shape == (size, size, 1)
    cv2.imwrite('train_A/' + sign_id + '.png', wrapped)

    # Illustration
    images = convert_from_path('illustrations/' + sign_id + '.pdf')
    assert len(images) == 1, "sign multiple images " + sign_id
    img = images[0]
    assert img is not None, "img is none " + sign_id
    img = convert_from_path('illustrations/' + sign_id + '.pdf')[0]
    wrapped = wrap_img(np.array(downscale(img)))[:, :, :1]
    assert wrapped.shape == (size, size, 1)
    cv2.imwrite('train_B/' + sign_id + '.png', wrapped)
