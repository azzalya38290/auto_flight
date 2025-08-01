import pydirectinput
import time
from core.window import focus_game_window

print(">>> Place Elite Dangerous au menu station (fenêtre au premier plan) <<<")
print(">>> Attente 5s avant l'envoi des touches S, S, puis Espace...")

time.sleep(5)
focus_game_window()
time.sleep(1)

print("Appui S (descendre 1)")
pydirectinput.keyDown('s')
time.sleep(0.15)
pydirectinput.keyUp('s')
time.sleep(2)

print("Appui S (descendre 2)")
pydirectinput.keyDown('s')
time.sleep(0.15)
pydirectinput.keyUp('s')
time.sleep(2)

print("Appui Espace (sélection)")
pydirectinput.keyDown('space')
time.sleep(0.15)
pydirectinput.keyUp('space')

print("Séquence terminée.")
