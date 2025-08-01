import pytesseract
import mss
import numpy as np
import cv2

def screenshot_game(window_region=None):
    with mss.mss() as sct:
        monitor = window_region or sct.monitors[1]
        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

def ocr_image(img):
    text = pytesseract.image_to_string(img, lang='eng')
    return text

if __name__ == "__main__":
    img = screenshot_game()
    text = ocr_image(img)
    print(text)
