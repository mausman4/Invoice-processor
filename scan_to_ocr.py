import pytesseract

def stt(PATH):
    return pytesseract.image_to_string(PATH)
