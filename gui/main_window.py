from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer
import sys

class MainWindow(QMainWindow):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.setWindowTitle("EliteBot - Contrôle Automatique ED")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()
        self.status_label = QLabel("État du vaisseau : inconnu")
        self.launch_btn = QPushButton("Décollage automatique")
        layout.addWidget(self.status_label)
        layout.addWidget(self.launch_btn)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        # Timer pour mise à jour de l'état toutes les secondes
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status_label)
        self.timer.start(1000)  # 1000 ms = 1 seconde

    def update_status_label(self):
        st = self.state.get_state()
        txt = (
            f"Système : {st['system']} | "
            f"Station : {st['station']} | "
            f"Docked : {st['docked']} | "
            f"Landed : {st['landed']}"
        )
        self.status_label.setText(txt)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    from core.state import GLOBAL_STATE
    win = MainWindow(GLOBAL_STATE)
    win.show()
    sys.exit(app.exec())
