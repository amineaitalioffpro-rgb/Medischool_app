# ui/prescription_medicament_form.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox,
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)

from services.medicament_service import MedicamentService
from services.prescription_medicament_service import PrescriptionMedicamentService


class PrescriptionMedicamentFormDialog(QDialog):
    def __init__(self, id_prescription: int, parent=None):
        super().__init__(parent)

        self.id_prescription = id_prescription

        self.setWindowTitle(f"Ajouter médicament à prescription #{id_prescription}")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Médicaments
        self.medicament = QComboBox()
        self.medicament_map = {}

        meds = MedicamentService.get_all()
        if not meds:
            self.medicament.addItem("Aucun médicament disponible")
        else:
            for m in meds:
                self.medicament.addItem(m.nom_medicament)
                self.medicament_map[m.nom_medicament] = m.id_medicament

        self.dose = QLineEdit()
        self.dose.setPlaceholderText("ex : 500mg")

        self.frequence = QLineEdit()
        self.frequence.setPlaceholderText("ex : 2 fois/jour")

        self.duree = QLineEdit()
        self.duree.setPlaceholderText("ex : 7 jours")

        form.addRow("Médicament :", self.medicament)
        form.addRow("Dose :", self.dose)
        form.addRow("Fréquence :", self.frequence)
        form.addRow("Durée :", self.duree)

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
        if not self.medicament_map:
            QMessageBox.warning(self, "Erreur", "Aucun médicament disponible.")
            return

        if not self.dose.text().strip():
            QMessageBox.warning(self, "Erreur", "Dose obligatoire.")
            return

        if not self.frequence.text().strip():
            QMessageBox.warning(self, "Erreur", "Fréquence obligatoire.")
            return

        if not self.duree.text().strip():
            QMessageBox.warning(self, "Erreur", "Durée obligatoire.")
            return

        nom = self.medicament.currentText()
        id_medicament = self.medicament_map.get(nom)

        data = {
            "id_prescription": self.id_prescription,
            "id_medicament": id_medicament,
            "dose": self.dose.text().strip(),
            "frequence": self.frequence.text().strip(),
            "duree": self.duree.text().strip()
        }

        ok = PrescriptionMedicamentService.add(data)

        if ok:
            QMessageBox.information(self, "OK", "Médicament ajouté.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible d'ajouter le médicament.")
