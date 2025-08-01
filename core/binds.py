import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Optional, List

# Chemin par défaut (à adapter selon utilisateur si besoin)
BINDS_FOLDER = Path(os.path.expandvars(
    r"C:\Users\mickael\AppData\Local\Frontier Developments\Elite Dangerous\Options\Bindings"
))

# Actions principales (ajoute/modifie si besoin)
ACTIONS = [
      'YawLeftButton',
            'YawRightButton',
            'RollLeftButton',
            'RollRightButton',
            'PitchUpButton',
            'PitchDownButton',
            'SetSpeedZero',
            'SetSpeed50',
            'SetSpeed100',
            'HyperSuperCombination',
            'SelectTarget',
            'DeployHeatSink',
            'UIFocus',
            'UI_Up',
            'UI_Down',
            'UI_Left',
            'UI_Right',
            'UI_Select',
            'UI_Back',
            'CycleNextPanel',
            'HeadLookReset',
            'PrimaryFire',
            'SecondaryFire',
            'ExplorationFSSEnter',
            'ExplorationFSSQuit',
            'MouseReset',
            'DeployHardpointToggle',
            'IncreaseEnginesPower',
            'IncreaseWeaponsPower',
            'IncreaseSystemsPower',
            'GalaxyMapOpen',
            'CamZoomIn',  # Gal map zoom in
            'SystemMapOpen',
            'UseBoostJuice',
            'Supercruise',
            'UpThrustButton',
            'LandingGearToggle',
            'TargetNextRouteSystem',  # Target next system in route
            'CamTranslateForward',
            'CamTranslateRight',
    # Ajoute ici toutes les actions utiles pour l'automatisation
]

class BindProfile:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.stem
        self.bindings = {}  # {Action: [Touches]}

    def load(self):
        if not self.path.exists():
            raise FileNotFoundError(f"Binds file not found: {self.path}")
        tree = ET.parse(self.path)
        root = tree.getroot()
        bindings = {}
        for action in ACTIONS:
            elem = root.find(f".//{action}")
            if elem is not None:
                keys = []
                for key in elem:
                    if key.tag.lower().endswith("key") or key.tag.lower().endswith("button"):
                        keys.append(key.text)
                bindings[action] = keys
        self.bindings = bindings

    def get_binding(self, action: str) -> Optional[List[str]]:
        return self.bindings.get(action)

    def __str__(self):
        return f"BindProfile({self.name})"

def list_bind_files() -> List[Path]:
    """Retourne la liste des fichiers .binds du dossier"""
    return sorted(BINDS_FOLDER.glob("*.binds"))

def get_latest_bind_file() -> Optional[Path]:
    """Retourne le chemin du dernier fichier .binds modifié"""
    files = list_bind_files()
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)

def load_active_profile() -> Optional[BindProfile]:
    """Charge automatiquement le profil le plus récent"""
    bind_path = get_latest_bind_file()
    if not bind_path:
        print("Aucun fichier .binds trouvé dans le dossier des bindings.")
        return None
    profile = BindProfile(bind_path)
    profile.load()
    print(f"[Binds] Profil actif chargé : {profile.name}")
    return profile

def choose_profile() -> Optional[BindProfile]:
    """Affiche tous les profils et laisse l'utilisateur choisir"""
    files = list_bind_files()
    if not files:
        print("Aucun fichier .binds trouvé.")
        return None
    print("Profils détectés :")
    for i, file in enumerate(files):
        print(f"  [{i}] {file.name}")
    idx = int(input("Choisis le numéro du profil à charger : "))
    path = files[idx]
    profile = BindProfile(path)
    profile.load()
    print(f"[Binds] Profil chargé : {profile.name}")
    return profile

# Exemple d'utilisation autonome
if __name__ == "__main__":
    profile = load_active_profile()
    if profile:
        print("Bindings détectés :")
        for action, keys in profile.bindings.items():
            print(f"  {action:25s}: {', '.join(keys) if keys else '-'}")
