from PySide6.QtWidgets import QTextEdit

class LogViewer(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("background: #111; color: #0f0;")
        self.append("[LogViewer] Démarré.")

    def add_log(self, text):
        self.append(text)
