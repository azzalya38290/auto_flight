import os
import xml.etree.ElementTree as ET
from pathlib import Path

# Ajoute tous les noms d’actions utiles ici :
ACTIONS = [
    "UI_Down",
    "UI_Select",
    "UI_Up",
    "UI_Back",
    "Launch",
    "EngineBoost",
    "Supercruise",
    # Ajoute les autres actions de ton bot si besoin
]

BINDS_FOLDER = Path(os.path.expandvars(
    r"C:\Users\mickael\AppData\Local\Frontier Developments\Elite Dangerous\Options\Bindings"
))

def get_latest_binds_file() -> Path:
    files = sorted(BINDS_FOLDER.glob("*.binds"))
    if not files:
        raise FileNotFoundError("Aucun fichier .binds trouvé")
    return max(files, key=lambda f: f.stat().st_mtime)

class BindProfile:
    def __init__(self, path: Path):
        self.path = path
        self.bindings = self._parse_binds()

    def _parse_binds(self):
        tree = ET.parse(self.path)
        root = tree.getroot()
        bindings = {}
        for action in ACTIONS:
            elem = root.find(f".//{action}")
            if elem is not None:
                keys = []
                for key in elem:
                    if key.attrib.get("Device") == "Keyboard" and key.attrib.get("Key", "").startswith("Key_"):
                        # Par exemple "Key_S" => "keyboard_s"
                        keys.append("keyboard_" + key.attrib.get("Key")[4:].lower())
                if keys:
                    bindings[action] = keys
        return bindings

    def get_binding(self, action):
        return self.bindings.get(action, [])

def load_active_profile():
    path = get_latest_binds_file()
    print(f"[Binds] Profil actif chargé : {path.name}")
    return BindProfile(path)

# Mini-script debug
if __name__ == "__main__":
    profile = load_active_profile()
    if profile:
        print("Bindings détectés :")
        for action, keys in profile.bindings.items():
            print(f"  {action:25s}: {', '.join(keys) if keys else '-'}")
