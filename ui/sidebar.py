# ui/sidebar.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect


class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedWidth(250)
        self.setStyleSheet("""
            QWidget {
                background: #0d1117;
                border-right: 1px solid #1f2a35;
            }
            QLabel#titleLabel {
                color: #4da6ff;
                font-size: 26px;
                font-weight: bold;
                letter-spacing: 3px;
            }
            QPushButton#menuButton {
                background: transparent;
                color: #d6d6d6;
                padding: 14px;
                border: none;
                border-radius: 10px;
                font-size: 17px;
                text-align: left;
            }
            QPushButton#menuButton:hover {
                background: rgba(77,166,255,0.20);
                color: white;
                border-left: 3px solid rgba(77,166,255,0.6);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ----- TITRE -----
        title = QLabel("MEDISCHOOL")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Ligne décorative
        deco = QFrame()
        deco.setFrameShape(QFrame.Shape.HLine)
        deco.setStyleSheet("color:#2b3440; margin:12px;")
        layout.addWidget(deco)

        # Indicateur bleu
        self.indicator = QFrame(self)
        self.indicator.setGeometry(8, 100, 5, 46)
        self.indicator.setStyleSheet("background-color:#4da6ff; border-radius:3px;")

        self.anim = QPropertyAnimation(self.indicator, b"geometry")
        self.anim.setDuration(200)

        self.buttons = {}

        # ------------------------------
        #   LISTE SANS "Paramètres"
        # ------------------------------
        sections = [
            "Gestion des Élèves",
            "Dossiers Médicaux",
            "Consultations",
            "Personnel Médical",
            "Prescriptions",
            "Médicaments",
            "Rendez-vous",
            "Vaccinations",
            "Statistiques & Rapports"
        ]

        for s in sections:
            btn = QPushButton(s)
            btn.setObjectName("menuButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, b=btn: self.move_indicator(b))

            layout.addWidget(btn)
            self.buttons[s] = btn

        layout.addStretch()

    # Déplacement du marqueur bleu
    def move_indicator(self, btn):
        y = btn.y()
        h = btn.height()

        self.anim.stop()
        self.anim.setStartValue(self.indicator.geometry())
        self.anim.setEndValue(QRect(8, y, 5, h))
        self.anim.start()
