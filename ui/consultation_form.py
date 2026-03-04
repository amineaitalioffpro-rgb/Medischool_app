# ui/consultation_form.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QComboBox, QHBoxLayout, QMessageBox
)
from services.consultation_service import ConsultationService
  
from services.eleve_service import EleveService
from services.personnel_service import PersonnelService
import re


class ConsultationFormDialog(QDialog):
    def __init__(self, consultation=None, parent=None):
        """
        consultation = objet Consultation ou None
        - None  => mode ajout
        - objet => mode édition
        """
        super().__init__(parent)

        self.consultation = consultation
        self.is_edit = consultation is not None

        # Titre
        self.setWindowTitle(
            "Modifier Consultation" if self.is_edit else "Nouvelle Consultation"
        )
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # -----------------------------------------------------------
        #                   LISTE DES ÉLÈVES
        # -----------------------------------------------------------
        self.eleve = QComboBox()
        self.eleves_map = {}

        eleves = EleveService.get_all()

        if not eleves:
            self.eleve.addItem("Aucun élève disponible")
        else:
            for e in eleves:
                fullname = f"{e.nom} {e.prenom}"
                self.eleve.addItem(fullname)
                self.eleves_map[fullname] = e.id_eleve

        # -----------------------------------------------------------
        #               LISTE DU PERSONNEL MÉDICAL
        # -----------------------------------------------------------
        self.personnel = QComboBox()
        self.personnel_map = {}

        personnels = PersonnelService.get_all()

        if not personnels:
            self.personnel.addItem("Aucun personnel disponible")
        else:
            for p in personnels:
                fullname = f"{p.nom} {p.prenom}"
                self.personnel.addItem(fullname)
                self.personnel_map[fullname] = p.id_personnel

        # -----------------------------------------------------------
        #                   AUTRES CHAMPS
        # -----------------------------------------------------------
        self.date = QLineEdit()
        self.date.setPlaceholderText("YYYY-MM-DD")

        self.type = QComboBox()
        self.type.addItems(["Consultation", "Urgence", "Controle"])

        self.symptomes = QLineEdit()
        self.diagnostic = QLineEdit()

        # Décision → maintenant COMBOBOX OBLIGATOIRE
        self.decision = QComboBox()
        self.decision.addItems(["Repos", "Traitement", "Transfert"])

        # --- Ajout au formulaire ---
        form.addRow("Élève :", self.eleve)
        form.addRow("Personnel :", self.personnel)
        form.addRow("Date :", self.date)
        form.addRow("Type :", self.type)
        form.addRow("Symptômes :", self.symptomes)
        form.addRow("Diagnostic :", self.diagnostic)
        form.addRow("Décision :", self.decision)

        layout.addLayout(form)

        # Si mode édition → pré-remplir
        if self.is_edit:
            self._populate_from_consultation()

        # -----------------------------------------------------------
        #                         BOUTONS
        # -----------------------------------------------------------
        btns = QHBoxLayout()
        btn_save = QPushButton("Mettre à jour" if self.is_edit else "Enregistrer")
        btn_cancel = QPushButton("Annuler")

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

    # -----------------------------------------------------------
    #        Pré-remplir si on modifie
    # -----------------------------------------------------------
    def _populate_from_consultation(self):
        c = self.consultation

        # Élève
        for fullname, id_e in self.eleves_map.items():
            if id_e == c.id_eleve:
                index = self.eleve.findText(fullname)
                if index >= 0:
                    self.eleve.setCurrentIndex(index)

        # Personnel
        for fullname, id_p in self.personnel_map.items():
            if id_p == c.id_personnel:
                index = self.personnel.findText(fullname)
                if index >= 0:
                    self.personnel.setCurrentIndex(index)

        self.date.setText(c.date_consultation)
        self.type.setCurrentText(c.type_consultation)
        self.symptomes.setText(c.symptomes)
        self.diagnostic.setText(c.diagnostic)
        self.decision.setCurrentText(c.decisions)

    # -----------------------------------------------------------
    #                         SAVE()
    # -----------------------------------------------------------
    def save(self):

        # Vérification format date
        date_value = self.date.text().strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_value):
            QMessageBox.warning(self, "Erreur", "Format de date invalide (YYYY-MM-DD).")
            return

        if not self.symptomes.text().strip():
            QMessageBox.warning(self, "Erreur", "Veuillez saisir les symptômes.")
            return

        if not self.diagnostic.text().strip():
            QMessageBox.warning(self, "Erreur", "Veuillez saisir un diagnostic.")
            return

        # Préparation des données
        data = {
            "id_eleve": self.eleves_map.get(self.eleve.currentText()),
            "id_personnel": self.personnel_map.get(self.personnel.currentText()),
            "date_consultation": date_value,
            "type_consultation": self.type.currentText(),
            "symptomes": self.symptomes.text(),
            "diagnostic": self.diagnostic.text(),
            "decisions": self.decision.currentText()
        }

        # Ajout ou Update
        if self.is_edit:
            ok = ConsultationService.update(self.consultation.id_consultation, data)
        else:
            ok = ConsultationService.add(data)

        if ok:
            QMessageBox.information(
                self,
                "Succès",
                "Consultation mise à jour." if self.is_edit else "Consultation ajoutée."
            )
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Échec de l'opération.")
