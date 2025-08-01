import mss
import numpy as np
import cv2
import pytesseract

# À ADAPTER selon ta résolution pour lire le système à l'écran
OCR_REGION = {"top": 50, "left": 700, "width": 400, "height": 50}

def read_system_name():
    with mss.mss() as sct:
        img = np.array(sct.grab(OCR_REGION))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        # Prétraitement optionnel :
        _, img_bin = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(img_bin, config='--psm 6').strip()
        print(f"[OCR] Texte lu : '{text}'")
        return text
