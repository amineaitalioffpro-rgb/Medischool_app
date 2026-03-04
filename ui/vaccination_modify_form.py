# ui/vaccination_modify_form.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QComboBox, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

from services.vaccination_service import VaccinationService
from services.eleve_service import EleveService
from services.personnel_service import PersonnelService

import re


class VaccinationModifyDialog(QDialog):
    def __init__(self, id_vaccination: int):
        super().__init__()

        self.id_vaccination = id_vaccination
        self.setWindowTitle(f"Modifier Vaccination #{id_vaccination}")

        # 🔥 Correction lag : taille fixe + focus optimisé
        self.setFixedSize(420, 360)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setStyleSheet("QDialog { background-color: #1b1b1b; color: white; }")

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # =============================================
        #        Charger Vaccination depuis DB
        # =============================================
        self.vaccination = VaccinationService.get_by_id(id_vaccination)

        if not self.vaccination:
            QMessageBox.critical(self, "Erreur", "Vaccination introuvable.")
            self.reject()
            return

        # =============================================
        #               ÉLÈVES
        # =============================================
        self.eleve = QComboBox()
        self.eleve_map = {}

        eleves = EleveService.get_all()
        current_eleve_label = None

        for e in eleves:
            label = f"{e.id_eleve} - {e.nom} {e.prenom}"
            self.eleve.addItem(label)
            self.eleve_map[label] = e.id_eleve
            if e.id_eleve == self.vaccination.id_eleve:
                current_eleve_label = label

        if current_eleve_label:
            self.eleve.setCurrentText(current_eleve_label)

        # =============================================
        #               PERSONNEL
        # =============================================
        self.personnel = QComboBox()
        self.personnel_map = {}

        personnel = PersonnelService.get_all()
        current_personnel_label = None

        for p in personnel:
            label = f"{p.id_personnel} - {p.nom} {p.prenom}"
            self.personnel.addItem(label)
            self.personnel_map[label] = p.id_personnel
            if p.id_personnel == self.vaccination.id_personnel:
                current_personnel_label = label

        if current_personnel_label:
            self.personnel.setCurrentText(current_personnel_label)

        # =============================================
        #            INFOS VACCINATION
        # =============================================
        self.nom_vaccin = QLineEdit(self.vaccination.nom_vaccin)
        self.nom_vaccin.setPlaceholderText("Nom du vaccin")

        self.date_vaccin = QLineEdit(self.vaccination.date_vaccin)
        self.date_vaccin.setPlaceholderText("YYYY-MM-DD")

        self.rappel = QComboBox()
        self.rappel.addItems(["OUI", "NON"])
        self.rappel.setCurrentText(self.vaccination.rappel_necessaire)

        # Ajout au formulaire
        form.addRow("Élève :", self.eleve)
        form.addRow("Personnel :", self.personnel)
        form.addRow("Nom Vaccin :", self.nom_vaccin)
        form.addRow("Date Vaccin :", self.date_vaccin)
        form.addRow("Rappel nécessaire :", self.rappel)

        layout.addLayout(form)

        # =============================================
        #                BOUTONS
        # =============================================
        btns = QHBoxLayout()
        btn_save = QPushButton("Enregistrer")
        btn_cancel = QPushButton("Annuler")

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

        btn_save.setStyleSheet("background:#2d79c7; padding:6px; color:white;")
        btn_cancel.setStyleSheet("background:#555; padding:6px; color:white;")

        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

    # =============================================
    #                  SAVE()
    # =============================================
    def save(self):

        # Vérifier format date
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", self.date_vaccin.text().strip()):
            QMessageBox.warning(self, "Erreur", "Format date invalide (YYYY-MM-DD).")
            return

        data = {
            "id_vaccination": self.id_vaccination,
            "id_eleve": self.eleve_map[self.eleve.currentText()],
            "id_personnel": self.personnel_map[self.personnel.currentText()],
            "nom_vaccin": self.nom_vaccin.text().strip(),
            "date_vaccin": self.date_vaccin.text().strip(),
            "rappel_necessaire": self.rappel.currentText(),
        }

        ok = VaccinationService.update(data)

        if ok:
            QMessageBox.information(self, "Succès", "Vaccination mise à jour.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de mettre à jour la vaccination.")
