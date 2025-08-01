import sys
import threading
import signal

from core.binds import load_active_profile
from core.input import InputController
from core.journal import JournalWatcher
from core.state import GLOBAL_STATE
from core.automation import AutoPilot
from core.window import focus_game_window

from gui.main_window import MainWindow

from PySide6.QtWidgets import QApplication

# Logger simple (tu peux remplacer par utils.logger)
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

def on_journal_event(event):
    # Met à jour l'état global
    GLOBAL_STATE.update_from_event(event)

def start_journal_thread():
    watcher = JournalWatcher(on_event=on_journal_event)
    t = threading.Thread(target=watcher.run, daemon=True)
    t.start()
    return watcher, t

def main():
    focus_game_window()

    binds_profile = load_active_profile()
    if not binds_profile:
        logging.error("Impossible de charger les binds, arrêt du bot.")
        return

    input_ctrl = InputController(binds_profile)
    autopilot = AutoPilot(input_ctrl, GLOBAL_STATE)
    journal_watcher, journal_thread = start_journal_thread()

    app = QApplication(sys.argv)
    window = MainWindow(GLOBAL_STATE)

    # --- FONCTION DE DEBUG AVANT LE DÉCOLLAGE
    def gui_launch_sequence():
        print("[DEBUG STATE] Etat actuel :", GLOBAL_STATE.get_state())
        logging.info("Demande de décollage automatique via GUI.")
        autopilot.launch_sequence()
    window.launch_btn.clicked.connect(gui_launch_sequence)

    window.show()

    def exit_handler(sig, frame):
        logging.info("Arrêt du bot demandé. Arrêt du watcher journal...")
        journal_watcher.stop()
        app.quit()
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    app.exec()
    logging.info("Bot arrêté proprement.")

if __name__ == "__main__":
    main()
