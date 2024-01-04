import platform
from PIL import Image
from io import BytesIO
import cv2 
import pytesseract

from .base import GLOBAL

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = './applications/tesseract.exe'

img_path = "./sample_data/colgate-01.jpg"
img = cv2.imread(img_path)

def extract_text(img):
    extracted_data = pytesseract.image_to_string(img)

    return extracted_data

def perform_ocr(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error performing OCR: {str(e)}"
        )