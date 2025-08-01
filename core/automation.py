import time
from core.state import GLOBAL_STATE
from core.window import focus_game_window
from core.ocr import read_system_name

class AutoPilot:
    def __init__(self, input_controller, state=GLOBAL_STATE):
        self.input = input_controller
        self.state = state
        self.auto_mode_active = False
        self.destination = None

    def launch_sequence(self):
        print("[AutoPilot] Séquence de décollage (navigation Auto Launch).")
        state = self.state.get_state()
        if not state['docked']:
            print("[AutoPilot] Pas docké ! Séquence annulée.")
            return False
        focus_game_window()
        print("[AutoPilot] Attente 2s pour stabilisation du focus...")
        time.sleep(2)
        for i in range(2):
            print(f"[AutoPilot] Appui {i+1}/2 sur 'UI_Down'")
            ok = self.input.send_key("UI_Down", hold=0.2, focus=False)
            if not ok:
                print(f"[AutoPilot] Impossible d'envoyer 'UI_Down' ({i+1}/2).")
            time.sleep(2.5)
        print("[AutoPilot] Appui sur 'UI_Select' pour valider")
        ok = self.input.send_key("UI_Select", hold=0.2, focus=False)
        if not ok:
            print("[AutoPilot] Impossible d'envoyer 'UI_Select'.")
        else:
            print("[AutoPilot] Sélection Auto Launch envoyée.")
        time.sleep(2.5)
        print("[AutoPilot] Décollage terminé.")
        return True

    def landing_sequence(self):
        print("[AutoPilot] Séquence d’atterrissage (navigation Auto Dock).")
        state = self.state.get_state()
        if state['docked']:
            print("[AutoPilot] Déjà docké. Séquence annulée.")
            return False
        focus_game_window()
        print("[AutoPilot] Attente 2s pour stabilisation du focus...")
        time.sleep(2)
        for i in range(3):
            print(f"[AutoPilot] Appui {i+1}/3 sur 'UI_Down'")
            ok = self.input.send_key("UI_Down", hold=0.2, focus=False)
            if not ok:
                print(f"[AutoPilot] Impossible d'envoyer 'UI_Down' ({i+1}/3).")
            time.sleep(2.5)
        print("[AutoPilot] Appui sur 'UI_Select' pour valider")
        ok = self.input.send_key("UI_Select", hold=0.2, focus=False)
        if not ok:
            print("[AutoPilot] Impossible d'envoyer 'UI_Select'.")
        else:
            print("[AutoPilot] Sélection Auto Dock envoyée.")
        time.sleep(2.5)
        print("[AutoPilot] Atterrissage lancé.")
        return True

    def jump_sequence(self, system_name=None):
        print(f"[AutoPilot] Séquence de saut FSD vers '{system_name or 'destination'}'.")
        focus_game_window()
        time.sleep(2)
        # 1. Ouvre la Galaxy Map
        print("[AutoPilot] Ouvre la Galaxy Map")
        self.input.send_key("GalaxyMap", hold=0.2, focus=False)
        time.sleep(3)
        # 2. Recherche système
        if system_name:
            print(f"[AutoPilot] Recherche du système '{system_name}'")
            self.input.send_key("UI_Focus_Search", hold=0.2, focus=False)
            time.sleep(1.5)
            # Saisie du nom du système lettre par lettre
            import pydirectinput
            for c in system_name:
                if c == ' ':
                    pydirectinput.press('space')
                else:
                    pydirectinput.press(c.lower())
                time.sleep(0.15)
            # Valide la recherche
            pydirectinput.press('enter')
            time.sleep(2)
            # Sélectionne le système
            pydirectinput.press('enter')
            time.sleep(1)
        # 3. Ferme la carte
        print("[AutoPilot] Ferme la Galaxy Map")
        self.input.send_key("GalaxyMap", hold=0.2, focus=False)
        time.sleep(2)
        # 4. Lance le jump
        print("[AutoPilot] Lance le jump")
        self.input.send_key("HyperSuperCombination", hold=0.2, focus=False)
        time.sleep(8)
        print("[AutoPilot] Saut lancé.")
        return True

    def auto_loop(self, destination_system):
        print(f"[AutoPilot] MODE AUTO: Boucle décollage > saut > atterrissage vers {destination_system}")
        self.auto_mode_active = True
        self.destination = destination_system
        self.launch_sequence()
        # Optionnel : lecture OCR pour confirmation
        print("[AutoPilot] [OCR] Vérification du système actuel (post-décollage)...")
        current_sys = read_system_name()
        print(f"[AutoPilot] Système OCR lu : {current_sys}")
        self.jump_sequence(destination_system)
        time.sleep(2)
        print("[AutoPilot] [OCR] Vérification du système après saut...")
        current_sys = read_system_name()
        print(f"[AutoPilot] Système OCR lu : {current_sys}")
        self.landing_sequence()
        self.auto_mode_active = False
        print("[AutoPilot] MODE AUTO: Boucle terminée.")
