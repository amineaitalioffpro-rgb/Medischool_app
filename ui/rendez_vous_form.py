# ui/rendez_vous_form.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QPushButton,
    QComboBox, QHBoxLayout, QMessageBox, QDateEdit
)
from PyQt6.QtCore import QDate

from services.rendez_vous_service import RendezVousService
from services.eleve_service import EleveService
from services.personnel_service import PersonnelService


class RendezVousFormDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nouveau Rendez-vous")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # =====================================================
        #                   LISTE ELEVES
        # =====================================================
        self.cb_eleve = QComboBox()
        self.map_eleve = {}

        eleves = EleveService.get_all()
        if not eleves:
            self.cb_eleve.addItem("Aucun élève disponible")
        else:
            for e in eleves:
                label = f"{e.id_eleve} - {e.nom} {e.prenom}"
                self.cb_eleve.addItem(label)
                self.map_eleve[label] = e.id_eleve

        # =====================================================
        #                LISTE PERSONNEL
        # =====================================================
        self.cb_personnel = QComboBox()
        self.map_personnel = {}

        personnel = PersonnelService.get_all()
        if not personnel:
            self.cb_personnel.addItem("Aucun personnel disponible")
        else:
            for p in personnel:
                label = f"{p.id_personnel} - {p.nom} {p.prenom}"
                self.cb_personnel.addItem(label)
                self.map_personnel[label] = p.id_personnel

        # =====================================================
        #                     DATE
        # =====================================================
        self.date_rdv = QDateEdit()
        self.date_rdv.setDisplayFormat("yyyy-MM-dd")
        self.date_rdv.setDate(QDate.currentDate())

        # =====================================================
        #                  TYPE RDV
        # =====================================================
        self.cb_type = QComboBox()
        self.cb_type.addItems(["Consultation", "Urgence", "Controle"])

        # =====================================================
        #                  STATUT
        # =====================================================
        self.cb_statut = QComboBox()
        self.cb_statut.addItems(["Planifie", "Confirme", "Annule", "Termine"])

        # Ajout au formulaire
        form.addRow("Élève :", self.cb_eleve)
        form.addRow("Personnel :", self.cb_personnel)
        form.addRow("Date RDV :", self.date_rdv)
        form.addRow("Type RDV :", self.cb_type)
        form.addRow("Statut :", self.cb_statut)

        layout.addLayout(form)

        # =====================================================
        #                     BOUTONS
        # =====================================================
        btns = QHBoxLayout()
        btn_save = QPushButton("Enregistrer")
        btn_cancel = QPushButton("Annuler")

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

    # =====================================================
    #                        SAVE
    # =====================================================
    def save(self):
        selected_eleve = self.cb_eleve.currentText()
        selected_pers = self.cb_personnel.currentText()

        # Validation
        if selected_eleve not in self.map_eleve:
            QMessageBox.warning(self, "Erreur", "Élève invalide.")
            return

        if selected_pers not in self.map_personnel:
            QMessageBox.warning(self, "Erreur", "Personnel invalide.")
            return

        data = {
            "id_eleve": self.map_eleve[selected_eleve],
            "id_personnel": self.map_personnel[selected_pers],
            "date_rdv": self.date_rdv.date().toString("yyyy-MM-dd"),
            "type_rdv": self.cb_type.currentText(),
            "statut": self.cb_statut.currentText(),
        }

        ok = RendezVousService.add(data)

        if ok:
            QMessageBox.information(self, "Succès", "Rendez-vous ajouté.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Échec de l’ajout du rendez-vous.")
