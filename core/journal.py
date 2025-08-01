import os
import json
import time
from pathlib import Path
from typing import Callable, Dict, Any, Optional

JOURNAL_FOLDER = Path(os.path.expandvars(
    r"C:\Users\mickael\Saved Games\Frontier Developments\Elite Dangerous"
))

def get_latest_journal_file() -> Optional[Path]:
    """Détecte le dernier fichier journal créé."""
    files = sorted(JOURNAL_FOLDER.glob("Journal.*.log"))
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)

class JournalWatcher:
    def __init__(self, on_event: Callable[[Dict[str, Any]], None], sleep_time: float = 0.2):
        self.journal_file: Optional[Path] = get_latest_journal_file()
        self.on_event = on_event
        self.sleep_time = sleep_time
        self._running = False

    def _open_latest_file(self):
        self.journal_file = get_latest_journal_file()
        if not self.journal_file:
            raise FileNotFoundError("Aucun fichier journal Elite Dangerous trouvé.")
        print(f"[Journal] Suivi du fichier : {self.journal_file}")

    def run(self):
        self._open_latest_file()
        self._running = True
        with open(self.journal_file, "r", encoding="utf-8") as f:
            # 1. **Lis toutes les lignes EXISTANTES**
            for line in f:
                if line.strip():
                    try:
                        event = json.loads(line)
                        self.on_event(event)
                    except Exception as e:
                        print(f"[Journal] Erreur de parsing (init): {e} sur la ligne : {line}")

            # 2. Puis passe en mode "live" (tail -f)
            while self._running:
                line = f.readline()
                if line:
                    try:
                        event = json.loads(line)
                        self.on_event(event)
                    except Exception as e:
                        print(f"[Journal] Erreur de parsing : {e} sur la ligne : {line}")
                else:
                    time.sleep(self.sleep_time)
                    # Si le journal change (nouvelle session), recharge le dernier fichier
                    new_file = get_latest_journal_file()
                    if new_file != self.journal_file:
                        print(f"[Journal] Nouveau journal détecté : {new_file.name}")
                        f.close()
                        self.journal_file = new_file
                        f = open(self.journal_file, "r", encoding="utf-8")
                        f.seek(0, os.SEEK_END)

    def stop(self):
        self._running = False

# Exemple : Callback d’affichage simple
def print_event(event: Dict[str, Any]):
    # Filtrer certains events clefs
    event_type = event.get("event")
    important_events = [
        "Location", "FSDJump", "Docked", "Undocked", "SupercruiseEntry", "SupercruiseExit", "Touchdown", "Liftoff"
    ]
    if event_type in important_events:
        print(f">>> {event_type} : {json.dumps(event, indent=2)}")

if __name__ == "__main__":
    # Lancement direct (test)
    watcher = JournalWatcher(on_event=print_event)
    try:
        watcher.run()
    except KeyboardInterrupt:
        watcher.stop()
        print("\n[Journal] Arrêt du watcher.")
