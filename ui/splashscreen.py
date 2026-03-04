from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

class MedicalSplash(QSplashScreen):
    def __init__(self):
        # Charge l’image depuis le dossier assets
        pixmap = QPixmap("assets/splash_blue.png")
        super().__init__(pixmap)

        # Texte en bas
        self.setFont(QFont("Segoe UI", 11))
        self.showMessage(
            "Chargement de MediSchool Manager...",
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
            Qt.GlobalColor.white
        )
