import time
from core.state import GLOBAL_STATE

class AutoPilot:
    def __init__(self, input_controller, state=GLOBAL_STATE):
        self.input = input_controller
        self.state = state

    def launch_sequence(self):
        # Décollage automatique
        print("[AutoPilot] Séquence de décollage lancée.")
        if not self.state.get_state()['docked']:
            print("[AutoPilot] Pas docké ! Séquence annulée.")
            return False
        # 1. Relève le train d’atterrissage si besoin
        self.input.send_key("Launch") or self.input.send_key("UI_Select")
        time.sleep(6)  # Laisse le temps au vaisseau de sortir
        # 2. Boost pour sortir rapidement
        self.input.send_key("EngineBoost")
        print("[AutoPilot] Décollage terminé.")
        return True

    # Tu peux ajouter ici : travel_sequence, landing_sequence, etc.
