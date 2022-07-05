import pytesseract as tess
from PIL import Image


def print_all(image_file):
    print('\nstring\n', tess.image_to_string(image_file))
    print('\nboxes\n', tess.image_to_boxes(image_file))
    print('\ndata\n', tess.image_to_data(image_file))


# img1 = Image.open('img-eg-1.png')
img2 = Image.open('img-eg-2.png')
print_all(img2)
