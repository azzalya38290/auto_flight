import time
from core.state import GLOBAL_STATE

class AutoPilot:
    def __init__(self, input_controller, state=GLOBAL_STATE):
        self.input = input_controller
        self.state = state

    def launch_sequence(self):
        print("[AutoPilot] Séquence de décollage (navigation Auto Launch).")
        state = self.state.get_state()
        if not state['docked']:
            print("[AutoPilot] Pas docké ! Séquence annulée.")
            return False

        # Pause AVANT de commencer (laisse le temps au focus de bien s'installer)
        print("[AutoPilot] Attente 3s avant la séquence.")
        time.sleep(3)

        for i in range(2):
            print(f"[AutoPilot] Appui {i+1}/2 sur 'UI_Down'")
            ok = self.input.send_key("UI_Down", hold=0.2)
            if not ok:
                print(f"[AutoPilot] Impossible d'envoyer 'UI_Down' ({i+1}/2).")
            time.sleep(2.5)  # Pause rallongée

        print("[AutoPilot] Appui sur 'UI_Select' pour valider")
        ok = self.input.send_key("UI_Select", hold=0.2)
        if not ok:
            print("[AutoPilot] Impossible d'envoyer 'UI_Select'.")
        else:
            print("[AutoPilot] Sélection Auto Launch envoyée.")
        time.sleep(2.5)  # Pause après sélection

        print("[AutoPilot] Décollage terminé.")
        return True
