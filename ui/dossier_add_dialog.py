# ui/dossier_add_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
)
from services.dossier_service import DossierService


class DossierAddDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ajouter un dossier médical")
        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.id_eleve = QLineEdit()
        self.antecedents = QLineEdit()
        self.allergies = QLineEdit()
        self.note = QLineEdit()

        form.addRow("ID Élève :", self.id_eleve)
        form.addRow("Antécédents :", self.antecedents)
        form.addRow("Allergies :", self.allergies)
        form.addRow("Note médicale :", self.note)

        layout.addLayout(form)

        btn = QPushButton("Ajouter")
        btn.clicked.connect(self.save)
        layout.addWidget(btn)

    def save(self):
        try:
            data = {
                "id_eleve": int(self.id_eleve.text()),
                "antecedents": self.antecedents.text(),
                "allergies": self.allergies.text(),
                "note_medicale": int(self.note.text())
            }

            if DossierService.add(data):
                QMessageBox.information(self, "Succès", "Dossier ajouté !")
                self.accept()
            else:
                QMessageBox.warning(self, "Erreur", "Échec de l’ajout.")
        except:
            QMessageBox.warning(self, "Erreur", "Données invalides.")
