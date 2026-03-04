# ui/medicament_form.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox
)
from services.medicament_service import MedicamentService


class MedicamentFormDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ajouter Médicament")
        self.setFixedSize(380, 220)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.nom = QLineEdit()
        self.effets = QLineEdit()

        form.addRow("Nom :", self.nom)
        form.addRow("Effets Secondaires :", self.effets)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_save = QPushButton("Ajouter")
        btn_cancel = QPushButton("Annuler")

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

    def save(self):
        if not self.nom.text().strip():
            QMessageBox.warning(self, "Erreur", "Nom obligatoire.")
            return

        data = {
            "nom_medicament": self.nom.text().strip(),
            "effets_secondaires": self.effets.text().strip(),
        }

        ok = MedicamentService.add(data)

        if ok:
            QMessageBox.information(self, "Succès", "Médicament ajouté.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible d’ajouter.")
