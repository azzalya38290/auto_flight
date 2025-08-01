import threading
from typing import Optional, Dict, Any, Callable, List

class ShipState:
    def __init__(self):
        # État courant du vaisseau/joueur
        self.lock = threading.Lock()
        self.system: Optional[str] = None
        self.body: Optional[str] = None
        self.station: Optional[str] = None
        self.docked: bool = False
        self.landed: bool = False
        self.supercruise: bool = False
        self.in_space: bool = False
        self.coords: Optional[Dict[str, float]] = None
        self.last_event: Optional[Dict[str, Any]] = None
        self.last_event_type: Optional[str] = None
        self.destination: Optional[str] = None  # à étendre avec un vrai planner
        self.subscribers: List[Callable[[str, Dict[str, Any]], None]] = []

    def update_from_event(self, event: Dict[str, Any]):
        with self.lock:
            etype = event.get("event")
            self.last_event = event
            self.last_event_type = etype

            # Location (à l'arrivée dans le jeu ou après un jump)
            if etype == "Location":
                self.system = event.get("StarSystem")
                self.body = event.get("Body")
                self.coords = event.get("StarPos")
                self.station = event.get("StationName")
                self.docked = event.get("Docked", False)
                self.landed = event.get("Landed", False)
                self.supercruise = False
                self.in_space = not self.docked and not self.landed
            # FSDJump (changement de système)
            elif etype == "FSDJump":
                self.system = event.get("StarSystem")
                self.body = None
                self.coords = event.get("StarPos")
                self.station = None
                self.docked = False
                self.landed = False
                self.supercruise = False
                self.in_space = True
            # Docked
            elif etype == "Docked":
                self.station = event.get("StationName")
                self.body = event.get("Body")
                self.docked = True
                self.landed = False
                self.in_space = False
            # Undocked
            elif etype == "Undocked":
                self.station = None
                self.docked = False
                self.in_space = True
            # SupercruiseEntry
            elif etype == "SupercruiseEntry":
                self.supercruise = True
                self.in_space = True
            # SupercruiseExit
            elif etype == "SupercruiseExit":
                self.supercruise = False
                self.in_space = True
                self.body = event.get("Body")
            # Touchdown (atterrissage sur une planète)
            elif etype == "Touchdown":
                self.landed = True
                self.body = event.get("Body")
                self.in_space = False
            # Liftoff (redécollage)
            elif etype == "Liftoff":
                self.landed = False
                self.in_space = True
            # ApproachBody (approche d'une planète ou d'un astre)
            elif etype == "ApproachBody":
                self.body = event.get("Body")
            # ApproachSettlement (approche d'une base planétaire)
            elif etype == "ApproachSettlement":
                self.body = event.get("Body")
                self.station = event.get("Name")
            # DockingRequested (future extension)
            # DockingGranted (future extension)
            # TODO : ajouter tous les events nécessaires au fur et à mesure

            self._notify_subscribers(etype, event)

    def get_state(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "system": self.system,
                "body": self.body,
                "station": self.station,
                "docked": self.docked,
                "landed": self.landed,
                "supercruise": self.supercruise,
                "in_space": self.in_space,
                "coords": self.coords,
                "last_event_type": self.last_event_type,
                "destination": self.destination
            }

    def set_destination(self, destination: str):
        with self.lock:
            self.destination = destination

    def subscribe(self, callback: Callable[[str, Dict[str, Any]], None]):
        """Permet à d'autres modules ou à la GUI de s'abonner aux changements d'état."""
        self.subscribers.append(callback)

    def _notify_subscribers(self, event_type: str, event: Dict[str, Any]):
        for cb in self.subscribers:
            cb(event_type, event)

# Singleton pour l'ensemble du bot
GLOBAL_STATE = ShipState()

# Exemple d'utilisation :
if __name__ == "__main__":
    def print_state(event_type, event):
        print(f"[STATE] Event: {event_type}")
        print(GLOBAL_STATE.get_state())

    GLOBAL_STATE.subscribe(print_state)

    # Simule quelques événements :
    GLOBAL_STATE.update_from_event({"event": "Location", "StarSystem": "Sol", "Body": "Earth", "Docked": True, "StationName": "Galileo"})
    GLOBAL_STATE.update_from_event({"event": "Undocked"})
    GLOBAL_STATE.update_from_event({"event": "FSDJump", "StarSystem": "Alpha Centauri", "StarPos": [1.0, 2.0, 3.0]})
    GLOBAL_STATE.update_from_event({"event": "Docked", "StationName": "Hutton Orbital", "Body": "Alpha Centauri B 2"})
