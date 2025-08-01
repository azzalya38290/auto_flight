import time
try:
    import pyvjoy  # Pour l'émulation HOTAS/joystick
except ImportError:
    pyvjoy = None
try:
    import pydirectinput  # Pour l'émulation clavier/souris (plus fiable que pyautogui pour les jeux)
except ImportError:
    pydirectinput = None

class InputController:
    def __init__(self, binds):
        self.binds = binds  # Instance de BindProfile
        self.use_vjoy = pyvjoy is not None
        self.use_directinput = pydirectinput is not None

    def send_key(self, action, hold=0.1):
        keys = self.binds.get_binding(action)
        if not keys:
            print(f"[Input] Aucun bind trouvé pour l'action : {action}")
            return False

        key = keys[0]  # On prend le premier bind (à améliorer si multi-bind)
        if self.use_directinput:
            print(f"[Input] Send key via pydirectinput : {key}")
            pydirectinput.keyDown(key)
            time.sleep(hold)
            pydirectinput.keyUp(key)
            return True
        else:
            print(f"[Input] Fallback (non implémenté) : {key}")
            # Ici tu peux rajouter pyautogui ou autre
            return False

    def send_vjoy(self, button_id, duration=0.1):
        if not self.use_vjoy:
            print("[Input] vJoy non disponible.")
            return False
        joystick = pyvjoy.VJoyDevice(1)
        joystick.set_button(button_id, 1)
        time.sleep(duration)
        joystick.set_button(button_id, 0)
        return True

# À étendre avec les méthodes HOTAS, axes, etc.
