# ui/vaccination_form.py

from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QDialogButtonBox,
    QComboBox, QLineEdit, QDateEdit, QMessageBox
)
from PyQt6.QtCore import QDate

from services.vaccination_service import VaccinationService
from services.eleve_service import EleveService
from services.personnel_service import PersonnelService


class VaccinationFormDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ajouter une vaccination")

        layout = QFormLayout(self)

        self.eleve_combo = QComboBox()
        self.personnel_combo = QComboBox()
        self.nom_vaccin_input = QLineEdit()
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        self.rappel_combo = QComboBox()
        self.rappel_combo.addItems(["OUI", "NON"])

        self._load_eleves()
        self._load_personnel()

        layout.addRow("Élève :", self.eleve_combo)
        layout.addRow("Personnel :", self.personnel_combo)
        layout.addRow("Nom vaccin :", self.nom_vaccin_input)
        layout.addRow("Date vaccin :", self.date_edit)
        layout.addRow("Rappel nécessaire :", self.rappel_combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)

    def _load_eleves(self):
        self.eleves = EleveService.get_all()
        self.eleve_combo.clear()
        for e in self.eleves:
            self.eleve_combo.addItem(f"{e.nom} {e.prenom}", e.id_eleve)

    def _load_personnel(self):
        self.personnels = PersonnelService.get_all()
        self.personnel_combo.clear()
        for p in self.personnels:
            self.personnel_combo.addItem(f"{p.nom} {p.prenom}", p.id_personnel)

    def save(self):
        if not self.nom_vaccin_input.text().strip():
            QMessageBox.warning(self, "Attention", "Le nom du vaccin est obligatoire.")
            return

        data = {
            "id_eleve": self.eleve_combo.currentData(),
            "id_personnel": self.personnel_combo.currentData(),
            "nom_vaccin": self.nom_vaccin_input.text().strip(),
            "date_vaccin": self.date_edit.date().toString("yyyy-MM-dd"),
            "rappel_necessaire": self.rappel_combo.currentText()
        }

        ok = VaccinationService.add(data)
        if ok:
            QMessageBox.information(self, "Succès", "Vaccination ajoutée.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "L’ajout a échoué.")
