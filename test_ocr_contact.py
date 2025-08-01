import cv2
import numpy as np
import mss
import pytesseract
import time

# OCR REGION (à ajuster à ton HUD)
REGION = {"top": 1010, "left": 60, "width": 420, "height": 170}
DELAY_BETWEEN_FRAMES = 100000  # ms

print("---- HUD FULL PREVIEW MODE ----")
print("Use arrow keys to move the OCR region. +/- to resize height, </> to resize width.")
print("Press 'p' to pause/resume, 's' to save, 'q' to quit.")

def clamp(val, vmin, vmax):
    return max(vmin, min(val, vmax))

def draw_overlay(hud_img, region, ocr_text):
    overlay = hud_img.copy()
    cv2.rectangle(
        overlay,
        (region["left"], region["top"]),
        (region["left"] + region["width"], region["top"] + region["height"]),
        (0, 255, 80), 3
    )
    text_y = region["top"] - 10 if region["top"] > 30 else region["top"] + region["height"] + 25
    cv2.putText(
        overlay,
        f"OCR: {ocr_text}",
        (region["left"] + 5, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (50, 255, 90),
        2,
        cv2.LINE_AA
    )
    cv2.putText(
        overlay,
        f"Region: {region}",
        (15, 28),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (240, 200, 180),
        2,
        cv2.LINE_AA
    )
    return overlay

def save_png(img, region):
    ts = int(time.time())
    fname = f"hud_full_{region['left']}x{region['top']}_{region['width']}x{region['height']}_{ts}.png"
    cv2.imwrite(fname, img)
    print(f"[Saved] {fname}")

paused = False

with mss.mss() as sct:
    mon = sct.monitors[1]
    FULL_REGION = {
        "top": mon["top"], "left": mon["left"],
        "width": mon["width"], "height": mon["height"]
    }
    last_overlay = None

    while True:
        if not paused:
            full_img = np.array(sct.grab(FULL_REGION))
            ocr_crop = full_img[
                REGION["top"]:REGION["top"]+REGION["height"],
                REGION["left"]:REGION["left"]+REGION["width"]
            ]
            ocr_img = cv2.cvtColor(ocr_crop, cv2.COLOR_BGRA2GRAY)
            _, ocr_bin = cv2.threshold(ocr_img, 100, 255, cv2.THRESH_BINARY)
            text = pytesseract.image_to_string(ocr_bin, config='--psm 7').strip()
            if text: text = text.split("\n")[0]
            overlay = draw_overlay(full_img, REGION, text)
            last_overlay = overlay.copy()
        else:
            overlay = last_overlay

        cv2.imshow("HUD Full Preview", overlay)
        print(f"\rREGION: {REGION} | OCR: '{text if not paused else '(paused)'}'", end="")

        key = cv2.waitKey(DELAY_BETWEEN_FRAMES) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('p'):
            paused = not paused
            print(" -- PAUSED" if paused else " -- RESUMED")
        elif key == ord('s'):
            save_png(overlay, REGION)
        elif key == 81: # left arrow
            REGION["left"] = clamp(REGION["left"] - 2, 0, FULL_REGION["width"]-10)
        elif key == 83: # right arrow
            REGION["left"] = clamp(REGION["left"] + 2, 0, FULL_REGION["width"]-10)
        elif key == 82: # up arrow
            REGION["top"] = clamp(REGION["top"] - 2, 0, FULL_REGION["height"]-10)
        elif key == 84: # down arrow
            REGION["top"] = clamp(REGION["top"] + 2, 0, FULL_REGION["height"]-10)
        elif key == ord('+') or key == ord('='):
            REGION["height"] = clamp(REGION["height"] + 2, 10, FULL_REGION["height"]-REGION["top"])
        elif key == ord('-') or key == ord('_'):
            REGION["height"] = clamp(REGION["height"] - 2, 10, FULL_REGION["height"]-REGION["top"])
        elif key == ord('.') or key == ord('>'):
            REGION["width"] = clamp(REGION["width"] + 2, 10, FULL_REGION["width"]-REGION["left"])
        elif key == ord(',') or key == ord('<'):
            REGION["width"] = clamp(REGION["width"] - 2, 10, FULL_REGION["width"]-REGION["left"])

cv2.destroyAllWindows()
print("\nBye!")
