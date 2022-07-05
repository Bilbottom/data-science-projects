import pytesseract as tess
from PIL import Image

# tess.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'


def print_all(image_file):
    print('\nstring\n', tess.image_to_string(image_file))
    print('\nboxes\n', tess.image_to_boxes(image_file))
    print('\ndata\n', tess.image_to_data(image_file))
    # print('\nosd\n', tess.image_to_osd(image_file))  # errors
    # print('\nalto_xml\n', tess.image_to_alto_xml(image_file))
    # print('\nget_output\n', tess.run_and_get_output(image_file))


def print_docstrings():
    print(tess.get_languages.__doc__)
    print(tess.get_tesseract_version.__doc__)
    print(tess.image_to_string.__doc__)
    print(tess.image_to_boxes.__doc__)
    print(tess.image_to_data.__doc__)
    print(tess.image_to_osd.__doc__)
    print(tess.image_to_alto_xml.__doc__)
    print(tess.run_and_get_output.__doc__)


# img1 = Image.open('img-eg-1.png')
img2 = Image.open('img-eg-2.png')

print_all(img2)
