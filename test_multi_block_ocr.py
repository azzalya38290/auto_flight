import cv2
import numpy as np
import mss
import pytesseract
import json
import time
import os

N_BLOCKS = 1
WIDTH, HEIGHT = 340, 40   # à adapter pour chaque zone

def select_points(image, block_idx):
    points = []

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            cv2.circle(img_display, (x, y), 5, (0, 255, 80), -1)
            cv2.putText(img_display, str(len(points)), (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,80), 2)
            cv2.imshow(f"Select 4 corners for block {block_idx+1}", img_display)
    img_display = image.copy()
    cv2.imshow(f"Select 4 corners for block {block_idx+1}", img_display)
    cv2.setMouseCallback(f"Select 4 corners for block {block_idx+1}", click_event)

    print(f"\nClique (dans l'ordre) les 4 coins du bloc {block_idx+1} : haut-gauche, haut-droit, bas-droit, bas-gauche.")
    while len(points) < 4:
        cv2.waitKey(1)
    cv2.destroyWindow(f"Select 4 corners for block {block_idx+1}")
    return np.float32(points)

def ocr_deskew_block(image, src_points, width, height, thresh=140, psm=7):
    dst_points = np.float32([
        [0, 0], [width, 0], [width, height], [0, height]
    ])
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    deskewed = cv2.warpPerspective(image, matrix, (width, height))
    img_gray = cv2.cvtColor(deskewed, cv2.COLOR_BGRA2GRAY)
    _, img_bin = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(img_bin, config=f'--psm {psm}').strip()
    return deskewed, img_bin, text

def save_points(block_points, filename="ocr_blocks_points.json"):
    with open(filename, "w") as f:
        json.dump([pts.tolist() for pts in block_points], f)
    print(f"[Saved] Les points des blocs ont été sauvegardés dans {filename}")

def load_points(filename="ocr_blocks_points.json"):
    with open(filename, "r") as f:
        pts = json.load(f)
    return [np.float32(p) for p in pts]

def save_block_screenshot(image, points, block_idx, outdir="ocr_block_screens"):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    img_copy = image.copy()
    pts = points.astype(int)
    color = (0, 220, 220)
    # Trace les points
    for i, (x, y) in enumerate(pts):
        cv2.circle(img_copy, (x, y), 6, color, -1)
        cv2.putText(img_copy, str(i+1), (x+8, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    # Trace le polygone
    cv2.polylines(img_copy, [pts], isClosed=True, color=color, thickness=2)
    fname = os.path.join(outdir, f"block_{block_idx+1}_zone.png")
    cv2.imwrite(fname, img_copy)
    print(f"[Screenshot] Zone du bloc {block_idx+1} sauvegardée sous {fname}")

if __name__ == "__main__":
    with mss.mss() as sct:
        mon = sct.monitors[1]
        full_img = np.array(sct.grab({
            "top": mon["top"], "left": mon["left"],
            "width": mon["width"], "height": mon["height"]
        }))

    print("\nHUD capturé. Nombre de blocs à ajuster:", N_BLOCKS)
    block_points = []
    for block_idx in range(N_BLOCKS):
        pts = select_points(full_img, block_idx)
        block_points.append(pts)
        # Sauvegarde screenshot annoté tout de suite
        save_block_screenshot(full_img, pts, block_idx)
        deskewed, img_bin, text = ocr_deskew_block(full_img, pts, WIDTH, HEIGHT)
        print(f"\nBloc {block_idx+1} OCR (deskewé): '{text}'")
        cv2.imshow(f"Block {block_idx+1} - deskewed", deskewed)
        cv2.imshow(f"Block {block_idx+1} - binarized", img_bin)
        print("Appuie sur une touche pour continuer au prochain bloc...")
        cv2.waitKey(0)
        cv2.destroyWindow(f"Block {block_idx+1} - deskewed")
        cv2.destroyWindow(f"Block {block_idx+1} - binarized")

    # Option : sauvegarder les points pour plus tard
    save = input("Sauvegarder les points sélectionnés ? (y/n) : ").strip().lower()
    if save == "y":
        save_points(block_points)

    print("\n--- Fini ! Les zones deskewées, l'OCR et les screenshots de chaque bloc ont été affichés et sauvegardés. ---")
