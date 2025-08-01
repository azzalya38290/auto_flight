import sys
import threading
import signal

from core.binds import load_active_profile
from core.input import InputController
from core.journal import JournalWatcher
from core.state import GLOBAL_STATE
from core.automation import AutoPilot
from gui.main_window import MainWindow

from PySide6.QtWidgets import QApplication
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

main_autopilot = None

def on_journal_event(event):
    GLOBAL_STATE.update_from_event(event)
    etype = event.get("event")
    if main_autopilot and main_autopilot.auto_mode_active:
        if etype == "Undocked":
            print("[Journal] Event Undocked détecté (auto-mode)")
            main_autopilot.jump_sequence(main_autopilot.destination)
        elif etype == "FSDJump":
            print("[Journal] Event FSDJump détecté (auto-mode)")
            main_autopilot.landing_sequence()

def start_journal_thread():
    watcher = JournalWatcher(on_event=on_journal_event)
    t = threading.Thread(target=watcher.run, daemon=True)
    t.start()
    return watcher, t

def main():
    global main_autopilot
    binds_profile = load_active_profile()
    if not binds_profile:
        logging.error("Impossible de charger les binds, arrêt du bot.")
        return
    input_ctrl = InputController(binds_profile)
    main_autopilot = AutoPilot(input_ctrl, GLOBAL_STATE)
    journal_watcher, journal_thread = start_journal_thread()
    app = QApplication(sys.argv)
    window = MainWindow(GLOBAL_STATE, main_autopilot)
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
