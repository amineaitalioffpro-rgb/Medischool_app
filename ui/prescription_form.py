# ui/prescription_form.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QTextEdit, QPushButton, QHBoxLayout, QMessageBox
)

from services.prescription_service import PrescriptionService
from services.consultation_service import ConsultationService


class PrescriptionFormDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Nouvelle Prescription")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # ----------------------------------------------------
        #        LISTE DES CONSULTATIONS DISPONIBLES
        # ----------------------------------------------------
        self.consultation = QLineEdit()
        self.consultation.setPlaceholderText("ID Consultation (ex: 1)")

        # ----------------------------------------------------
        #                  INSTRUCTIONS
        # ----------------------------------------------------
        self.instructions = QTextEdit()
        self.instructions.setPlaceholderText("Instructions médicales...")

        # Ajout au formulaire
        form.addRow("ID Consultation :", self.consultation)
        form.addRow("Instructions :", self.instructions)

        layout.addLayout(form)

        # ----------------------------------------------------
        #                   BOUTONS
        # ----------------------------------------------------
        btns = QHBoxLayout()
        btn_save = QPushButton("Enregistrer")
        btn_cancel = QPushButton("Annuler")

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

    # ----------------------------------------------------
    #                      SAVE
    # ----------------------------------------------------
    def save(self):

        # --- Vérif ID consultation ---
        if not self.consultation.text().strip().isdigit():
            QMessageBox.warning(self, "Erreur", "ID consultation invalide.")
            return

        id_consult = int(self.consultation.text().strip())

        # Vérifier si l’ID consultation existe vraiment
        check = ConsultationService.get_by_id(id_consult)
        if not check:
            QMessageBox.warning(self, "Erreur", "Cette consultation n’existe pas.")
            return

        # --- Vérif instructions ---
        if not self.instructions.toPlainText().strip():
            QMessageBox.warning(self, "Erreur", "Les instructions sont obligatoires.")
            return

        data = {
            "id_consultation": id_consult,
            "instructions": self.instructions.toPlainText().strip()
        }

        ok = PrescriptionService.add(data)

        if ok:
            QMessageBox.information(self, "Succès", "Prescription ajoutée.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible d'ajouter la prescription.")
