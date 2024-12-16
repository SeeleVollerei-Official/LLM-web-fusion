from PIL import Image
import pytesseract


def image2text(filename):
    image = Image.open(f'../save/{filename}')
    config = "-l chi_sim --oem 2 --psm 12"
    # 使用 pytesseract 进行 OCR
    text = pytesseract.image_to_string(image, config=config)

    return text
