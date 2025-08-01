from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class SettingsWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        layout = QVBoxLayout()
        self.label = QLabel("Chemin des binds:")
        self.path_edit = QLineEdit(config.get("binds_path", ""))
        self.save_btn = QPushButton("Sauvegarder")
        self.save_btn.clicked.connect(self.save)
        layout.addWidget(self.label)
        layout.addWidget(self.path_edit)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)

    def save(self):
        self.config["binds_path"] = self.path_edit.text()
        print("[Settings] Config sauvegardée :", self.config)
