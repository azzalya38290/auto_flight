import time

try:
    import pydirectinput  # Automatisation clavier/souris fiable pour les jeux
except ImportError:
    pydirectinput = None

class InputController:
    def __init__(self, binds):
        self.binds = binds  # Instance de BindProfile
        self.use_directinput = pydirectinput is not None

    def send_key(self, action, hold=0.15, focus=False):
        keys = self.binds.get_binding(action)
        if not keys:
            print(f"[Input] Aucun bind trouvé pour l'action : {action}")
            return False

        key = keys[0]
        print(f"[Input] Essai d'envoi de la touche/bouton '{key}' pour l'action '{action}'")

        if key and key.lower().startswith("keyboard_"):
            key_name = key[9:].lower()
            print(f"[Input] Utilisation de pydirectinput pour : {key_name}")
            if self.use_directinput:
                if focus:
                    from core.window import focus_game_window
                    focus_game_window()
                    time.sleep(0.1)
                pydirectinput.keyDown(key_name)
                time.sleep(hold)
                pydirectinput.keyUp(key_name)
                print(f"[Input] Touche '{key_name}' envoyée (pydirectinput)")
                return True
            else:
                print("[Input] PyDirectInput non disponible. Pas d'action.")
                return False

        elif key and key.lower().startswith("joy_"):
            print(f"[Input] Bind joystick détecté : {key} (NON GÉRÉ, AJOUTE UN BIND CLAVIER dans Elite Dangerous pour cette action !)")
            return False

        else:
            print(f"[Input] Type de bind inconnu ou non pris en charge : {key}")
            return False
