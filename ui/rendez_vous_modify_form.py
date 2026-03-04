# ui/rendez_vous_modify_form.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QComboBox, QHBoxLayout, QMessageBox
)
from services.rendez_vous_service import RendezVousService
from services.eleve_service import EleveService
from services.personnel_service import PersonnelService

import re


class RendezVousModifyDialog(QDialog):
    def __init__(self, id_rdv: int):
        super().__init__()

        self.id_rdv = id_rdv
        self.setWindowTitle(f"Modifier Rendez-vous #{id_rdv}")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # =============================================
        #        Charger RDV depuis la base
        # =============================================
        self.rdv = RendezVousService.get_by_id(id_rdv)

        if not self.rdv:
            QMessageBox.critical(self, "Erreur", "Rendez-vous introuvable.")
            self.reject()
            return

        # =============================================
        #              ELEVES
        # =============================================
        self.eleve = QComboBox()
        self.eleve_map = {}

        eleves = EleveService.get_all()

        current_eleve_label = None

        for e in eleves:
            label = f"{e.id_eleve} - {e.nom} {e.prenom}"
            self.eleve.addItem(label)
            self.eleve_map[label] = e.id_eleve

            if e.id_eleve == self.rdv.id_eleve:
                current_eleve_label = label

        if current_eleve_label:
            self.eleve.setCurrentText(current_eleve_label)

        # =============================================
        #            PERSONNEL
        # =============================================
        self.personnel = QComboBox()
        self.personnel_map = {}

        personnel = PersonnelService.get_all()
        current_personnel_label = None

        for p in personnel:
            label = f"{p.id_personnel} - {p.nom} {p.prenom}"
            self.personnel.addItem(label)
            self.personnel_map[label] = p.id_personnel

            if p.id_personnel == self.rdv.id_personnel:
                current_personnel_label = label

        if current_personnel_label:
            self.personnel.setCurrentText(current_personnel_label)

        # =============================================
        #            AUTRES CHAMPS
        # =============================================
        self.date_rdv = QLineEdit(self.rdv.date_rdv)
        self.date_rdv.setPlaceholderText("YYYY-MM-DD")

        self.type_rdv = QComboBox()
        self.type_rdv.addItems(["Consultation", "Urgence", "Controle"])
        self.type_rdv.setCurrentText(self.rdv.type_rdv)

        self.statut = QComboBox()
        self.statut.addItems(["Planifie", "Confirme", "Annule", "Termine"])
        self.statut.setCurrentText(self.rdv.statut)

        # Ajout au formulaire
        form.addRow("Élève :", self.eleve)
        form.addRow("Personnel :", self.personnel)
        form.addRow("Date RDV :", self.date_rdv)
        form.addRow("Type RDV :", self.type_rdv)
        form.addRow("Statut :", self.statut)

        layout.addLayout(form)

        # =============================================
        #                BOUTONS
        # =============================================
        btns = QHBoxLayout()
        btn_save = QPushButton("Enregistrer")
        btn_cancel = QPushButton("Annuler")

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

    # =============================================
    #                  SAVE()
    # =============================================
    def save(self):

        # Vérifier format date
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", self.date_rdv.text().strip()):
            QMessageBox.warning(self, "Erreur", "Format date invalide (YYYY-MM-DD).")
            return

        data = {
            "id_rdv": self.id_rdv,
            "id_eleve": self.eleve_map[self.eleve.currentText()],
            "id_personnel": self.personnel_map[self.personnel.currentText()],
            "date_rdv": self.date_rdv.text().strip(),
            "type_rdv": self.type_rdv.currentText(),
            "statut": self.statut.currentText(),
        }

        ok = RendezVousService.update(data)

        if ok:
            QMessageBox.information(self, "Succès", "Rendez-vous mis à jour.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de mettre à jour le rendez-vous.")
