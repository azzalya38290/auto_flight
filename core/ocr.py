import mss
import numpy as np
import cv2
import pytesseract

# Adjust these values for your screen/game HUD!
SYSTEM_NAME_REGION = {"top": 50, "left": 700, "width": 400, "height": 50}
CONTACT_LINE_REGION = {"top": 360, "left": 480, "width": 470, "height": 38}

def _show_preview(img, ocr_text, title="OCR Preview"):
    if ocr_text:
        ocr_text = ocr_text.split("\n")[0]
    window_title = f"{title}: '{ocr_text}'"
    cv2.imshow(window_title, img)
    # Wait: 1.5s or until user presses 'q'
    key = cv2.waitKey(1500)
    cv2.destroyAllWindows()

def read_system_name():
    """
    Capture the HUD region where the system name appears.
    Returns OCR text, and shows a preview image for debugging.
    """
    with mss.mss() as sct:
        img = np.array(sct.grab(SYSTEM_NAME_REGION))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        _, img_bin = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(img_bin, config='--psm 6').strip()
        print(f"[OCR] Read system name: '{text}'")
        _show_preview(img_bin, text, "System Name OCR")
        if text:
            text = text.split("\n")[0]
        return text

def read_contact_line():
    """
    Capture the highlighted line in the contacts list (left panel).
    Returns OCR text, and shows a preview image for debugging.
    """
    with mss.mss() as sct:
        img = np.array(sct.grab(CONTACT_LINE_REGION))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        _, img_bin = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(img_bin, config='--psm 7').strip()
        print(f"[OCR] Read contact line: '{text}'")
        _show_preview(img_bin, text, "Contact Line OCR")
        if text:
            text = text.split("\n")[0]
        return text
