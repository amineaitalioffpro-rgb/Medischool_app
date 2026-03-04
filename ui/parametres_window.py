# ui/parametres_window.py

import json
import os

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QCheckBox,
    QPushButton, QMessageBox, QLabel
)

SETTINGS_FILE = "settings.json"


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"access_dossier": True}
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"access_dossier": True}


def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)


class ParametresWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # =============================
        # Permissions
        # =============================
        self.box_permissions = QGroupBox("Permissions")
        perm_layout = QVBoxLayout(self.box_permissions)

        self.chk_access_dossier = QCheckBox(
            "Autoriser l'accès aux dossiers médicaux"
        )

        # charger la valeur réelle
        settings = load_settings()
        self.chk_access_dossier.setChecked(settings.get("access_dossier", True))

        perm_layout.addWidget(self.chk_access_dossier)

        btn_save = QPushButton("Sauvegarder les paramètres")
        btn_save.clicked.connect(self._save_settings)
        perm_layout.addWidget(btn_save)

        layout.addWidget(self.box_permissions)

        layout.addStretch()

    # =========================================
    # SAUVEGARDE SÉCURISÉE
    # =========================================
    def _save_settings(self):
        settings = {
            "access_dossier": self.chk_access_dossier.isChecked()
        }

        save_settings(settings)

        QMessageBox.information(
            self, "OK", "Paramètres sauvegardés avec succès."
        )
