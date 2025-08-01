from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout,
    QWidget, QLineEdit, QHBoxLayout, QCheckBox, QFileDialog, QTextEdit, QSizePolicy, QFrame
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont, QColor, QPalette

class MainWindow(QMainWindow):
    def __init__(self, state, autopilot):
        super().__init__()
        self.state = state
        self.autopilot = autopilot
        self.setWindowTitle("🚀 EliteBot - Automatisation Elite Dangerous")
        self.setMinimumSize(640, 500)
        self.setStyleSheet("""
            QWidget { background-color: #17191A; color: #D0D3D7; font-size: 16px; }
            QPushButton { 
                background: #292C31; color: #E6E7E9; 
                padding: 12px 24px; border-radius: 10px; 
                font-weight: 600; font-size: 17px; 
            }
            QPushButton:hover { background: #404248; }
            QLineEdit { 
                background: #232629; color: #ECECEC; 
                padding: 8px; border-radius: 6px; font-size: 16px;
            }
            QCheckBox { padding: 8px 0px; }
            QLabel { font-size: 16px; }
            QFrame#Separator { background: #33363A; min-height:2px; max-height:2px; }
            QTextEdit { background: #202225; color: #A9AFC2; font-size: 14px; border-radius: 6px; }
        """)

        # --- Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(18)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # --- Statut
        self.status_label = QLabel("État du vaisseau : inconnu")
        self.status_label.setFont(QFont("Segoe UI", 17, QFont.Bold))
        main_layout.addWidget(self.status_label)

        # --- Séparateur
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        sep1.setObjectName("Separator")
        main_layout.addWidget(sep1)

        # --- LIGNE D'ACTIONS
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.launch_btn = QPushButton("Décollage automatique")
        self.launch_btn.clicked.connect(self.launch_sequence)
        btn_layout.addWidget(self.launch_btn)

        self.landing_btn = QPushButton("Atterrissage automatique")
        self.landing_btn.clicked.connect(self.landing_sequence)
        btn_layout.addWidget(self.landing_btn)

        main_layout.addLayout(btn_layout)

        # --- Séquence de jump
        jump_layout = QHBoxLayout()
        jump_layout.setSpacing(8)
        self.jump_input = QLineEdit()
        self.jump_input.setPlaceholderText("Nom du système cible")
        jump_layout.addWidget(self.jump_input, stretch=2)
        self.jump_btn = QPushButton("Jump to system")
        self.jump_btn.clicked.connect(self.jump_to_system)
        jump_layout.addWidget(self.jump_btn, stretch=1)
        main_layout.addLayout(jump_layout)

        # --- Sauvegarde/chargement destination
        save_load_layout = QHBoxLayout()
        self.save_btn = QPushButton("Sauver destination")
        self.save_btn.clicked.connect(self.save_destination)
        save_load_layout.addWidget(self.save_btn)
        self.load_btn = QPushButton("Charger destination")
        self.load_btn.clicked.connect(self.load_destination)
        save_load_layout.addWidget(self.load_btn)
        main_layout.addLayout(save_load_layout)

        # --- Mode AUTO
        self.auto_checkbox = QCheckBox("Mode AUTO décollage/jump/atterrissage")
        self.auto_checkbox.stateChanged.connect(self.auto_mode_toggled)
        main_layout.addWidget(self.auto_checkbox)

        # --- Séparateur
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setObjectName("Separator")
        main_layout.addWidget(sep2)

        # --- LOGS (live)
        log_label = QLabel("Journal d'exécution")
        log_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        main_layout.addWidget(log_label)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMaximumHeight(160)
        self.log_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.log_box)

        # --- Central Widget
        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)

        # --- Timers
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status_label)
        self.timer.timeout.connect(self.flush_log_queue)
        self.timer.start(700)

        # --- Buffer pour logs
        self._log_buffer = []

    def update_status_label(self):
        st = self.state.get_state()
        txt = (
            f"🪐 Système : <b>{st['system']}</b>  |  "
            f"🏤 Station : <b>{st['station']}</b>  |  "
            f"<span style='color: {'#41d336' if st['docked'] else '#fa5d5d'};'>Docked : <b>{st['docked']}</b></span>  |  "
            f"<span style='color: {'#41d336' if st['landed'] else '#fa5d5d'};'>Landed : <b>{st['landed']}</b></span>"
        )
        self.status_label.setText(txt)

    # ---- LOGGING utils
    def log(self, msg, color="#C6DBF7"):
        self._log_buffer.append((msg, color))

    def flush_log_queue(self):
        if not self._log_buffer:
            return
        cursor = self.log_box.textCursor()
        for msg, color in self._log_buffer:
            self.log_box.setTextColor(QColor(color))
            self.log_box.append(msg)
        self._log_buffer.clear()
        self.log_box.moveCursor(cursor.End)

    # --- Actions (callback UI)
    def launch_sequence(self):
        self.log("⏫ [Décollage] Démarré.", "#b0f251")
        self.autopilot.launch_sequence()
        self.log("⏫ [Décollage] Terminé.", "#b0f251")

    def landing_sequence(self):
        self.log("⏬ [Atterrissage] Démarré.", "#ffc651")
        self.autopilot.landing_sequence()
        self.log("⏬ [Atterrissage] Terminé.", "#ffc651")

    def jump_to_system(self):
        system_name = self.jump_input.text().strip()
        if not system_name:
            self.log("⚠️ Aucun système cible indiqué.", "#e07171")
            return
        self.log(f"🛸 [Jump] vers {system_name} demandé.", "#51cbff")
        self.autopilot.jump_sequence(system_name)
        self.log(f"🛸 [Jump] vers {system_name} terminé.", "#51cbff")

    def auto_mode_toggled(self, state):
        if state:
            system_name = self.jump_input.text().strip()
            if not system_name:
                self.log("⚠️ Aucun système cible indiqué pour le mode auto.", "#e07171")
                self.auto_checkbox.setChecked(False)
                return
            self.log(f"🟢 [MODE AUTO] Boucle sur {system_name}", "#b8ec7d")
            self.autopilot.auto_loop(system_name)
            self.auto_checkbox.setChecked(False)
            self.log("🟢 [MODE AUTO] Terminé.", "#b8ec7d")
        else:
            self.log("[MODE AUTO] Désactivé.", "#e07171")

    def save_destination(self):
        system_name = self.jump_input.text().strip()
        if not system_name:
            self.log("⚠️ Aucun système cible à sauvegarder.", "#e07171")
            return
        fname, _ = QFileDialog.getSaveFileName(self, "Sauver destination", "", "TXT Files (*.txt)")
        if fname:
            with open(fname, 'w') as f:
                f.write(system_name)
            self.log(f"[GUI] Destination '{system_name}' sauvegardée dans {fname}", "#a0bff8")

    def load_destination(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Charger destination", "", "TXT Files (*.txt)")
        if fname:
            with open(fname, 'r') as f:
                system_name = f.read().strip()
            self.jump_input.setText(system_name)
            self.log(f"[GUI] Destination '{system_name}' chargée depuis {fname}", "#a0bff8")
