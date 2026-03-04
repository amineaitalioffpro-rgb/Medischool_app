# ui/medicament_modify_form.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QTextEdit, QPushButton, QHBoxLayout, QMessageBox
)
from services.medicament_service import MedicamentService


class MedicamentModifyDialog(QDialog):
    def __init__(self, id_medicament: int, parent=None):
        super().__init__(parent)

        self.id_medicament = id_medicament

        self.setWindowTitle(f"Modifier Médicament #{id_medicament}")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.nom = QLineEdit()
        self.effets = QTextEdit()

        # Charger données
        med = MedicamentService.get_by_id(id_medicament)
        if not med:
            QMessageBox.critical(self, "Erreur", "Médicament introuvable.")
            self.reject()
            return

        self.nom.setText(med.nom_medicament)
        self.effets.setText(med.effets_secondaires)

        form.addRow("Nom :", self.nom)
        form.addRow("Effets secondaires :", self.effets)

        layout.addLayout(form)

        # Boutons
        btns = QHBoxLayout()
        btn_save = QPushButton("Enregistrer")
        btn_cancel = QPushButton("Annuler")

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

    # ======================================================
    #                      SAVE()
    # ======================================================
    def save(self):

        if not self.nom.text().strip():
            QMessageBox.warning(self, "Erreur", "Nom obligatoire.")
            return

        data = {
            "nom_medicament": self.nom.text().strip(),
            "effets_secondaires": self.effets.toPlainText().strip()
        }

        
        ok = MedicamentService.update(self.id_medicament, data)

        if ok:
            QMessageBox.information(self, "Succès", "Médicament mis à jour.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de mettre à jour.")
