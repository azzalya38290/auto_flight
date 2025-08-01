import cv2
import numpy as np
import mss
import pytesseract

# System Name
SYSTEM_SRC_POINTS = np.float32([
    [73.0, 1238.0], [332.0, 1216.0], [341.0, 1246.0], [79.0, 1273.0]
])
SYSTEM_WIDTH, SYSTEM_HEIGHT = 270, 40

# Contact Line -- REMPLACE par tes points
CONTACT_SRC_POINTS = np.float32([
    [100.0, 1100.0], [350.0, 1090.0], [355.0, 1120.0], [105.0, 1130.0]
])
CONTACT_WIDTH, CONTACT_HEIGHT = 270, 40

def deskew_and_ocr(src_points, width, height, thresh=140, psm=7, show_preview=True, region_name="OCR Region"):
    with mss.mss() as sct:
        mon = sct.monitors[1]
        full_img = np.array(sct.grab({
            "top": mon["top"], "left": mon["left"],
            "width": mon["width"], "height": mon["height"]
        }))
        dst_points = np.float32([
            [0, 0], [width, 0], [width, height], [0, height]
        ])
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        deskewed = cv2.warpPerspective(full_img, matrix, (width, height))
        img_gray = cv2.cvtColor(deskewed, cv2.COLOR_BGRA2GRAY)
        _, img_bin = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(img_bin, config=f'--psm {psm}').strip()
        if show_preview:
            cv2.imshow(region_name, img_bin)
            cv2.waitKey(1200)
            cv2.destroyWindow(region_name)
        return text

def read_system_name(show_preview=True):
    text = deskew_and_ocr(SYSTEM_SRC_POINTS, SYSTEM_WIDTH, SYSTEM_HEIGHT, thresh=140, psm=7, show_preview=show_preview, region_name="System OCR")
    print(f"[OCR] System Name: '{text}'")
    return text

def read_contact_line(show_preview=True):
    text = deskew_and_ocr(CONTACT_SRC_POINTS, CONTACT_WIDTH, CONTACT_HEIGHT, thresh=140, psm=7, show_preview=show_preview, region_name="Contact OCR")
    print(f"[OCR] Contact Line: '{text}'")
    return text

if __name__ == "__main__":
    print("OCR SYSTEM NAME : ", read_system_name(show_preview=True))
    print("OCR CONTACT LINE : ", read_contact_line(show_preview=True))
