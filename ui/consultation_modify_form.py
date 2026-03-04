# ui/consultation_modify_form.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QComboBox, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from services.consultation_service import ConsultationService
from services.eleve_service import EleveService
from services.personnel_service import PersonnelService
import re

class ConsultationModifyDialog(QDialog):
    def __init__(self, consultation_id: int):
        super().__init__()

        self.consultation_id = consultation_id
        self.setWindowTitle(f"Modifier Consultation #{consultation_id}")
        self.setMinimumWidth(450)

        # ---- Style global clean ----
        self.setStyleSheet("""
            QDialog {
                background-color: #10141A;
                color: white;
            }
            QLabel {
                font-size: 15px;
            }
            QLineEdit, QComboBox {
                padding: 6px;
                border: 1px solid #2f3b4a;
                border-radius: 6px;
                background: #1b1f27;
                color: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #4da6ff;
            }
        """)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # ================================================
        # Charger données existantes
        # ================================================
        self.consultation = ConsultationService.get_by_id(consultation_id)

        if not self.consultation:
            QMessageBox.critical(self, "Erreur", "Consultation introuvable.")
            self.reject()
            return

        # ===================== Élèves =====================
        self.eleve = QComboBox()
        self.eleves_map = {}

        for e in EleveService.get_all():
            fullname = f"{e.nom} {e.prenom}"
            self.eleve.addItem(fullname)
            self.eleves_map[fullname] = e.id_eleve

        self.eleve.setCurrentText(self.consultation.nom_eleve)

        # ================== Personnel =====================
        self.personnel = QComboBox()
        self.personnel_map = {}

        for p in PersonnelService.get_all():
            fullname = f"{p.nom} {p.prenom}"
            self.personnel.addItem(fullname)
            self.personnel_map[fullname] = p.id_personnel

        self.personnel.setCurrentText(self.consultation.nom_personnel)

        # =================== Champs =======================
        self.date = QLineEdit(self.consultation.date_consultation)
        self.type = QComboBox()
        self.type.addItems(["Consultation", "Urgence", "Controle"])
        self.type.setCurrentText(self.consultation.type_consultation)

        self.symptomes = QLineEdit(self.consultation.symptomes)
        self.diagnostic = QLineEdit(self.consultation.diagnostic)

        self.decision = QComboBox()
        self.decision.addItems(["Repos", "Traitement", "Transfert"])
        self.decision.setCurrentText(self.consultation.decisions)

        # ---- Ajout au formulaire ----
        form.addRow("Élève :", self.eleve)
        form.addRow("Personnel :", self.personnel)
        form.addRow("Date :", self.date)
        form.addRow("Type :", self.type)
        form.addRow("Symptômes :", self.symptomes)
        form.addRow("Diagnostic :", self.diagnostic)
        form.addRow("Décision :", self.decision)

        layout.addLayout(form)

        # ======================================================
        #                 BOUTONS STYLE MEDISCHOOL
        # ======================================================
        btns = QHBoxLayout()

        btn_save = QPushButton("Enregistrer")
        btn_cancel = QPushButton("Annuler")

        # 🔥 CORRECTION ICI
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #4da6ff;
                color: black;
                padding: 8px 14px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #72baff;
            }
        """)

        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #2a2f3a;
                color: white;
                padding: 8px 14px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3a3f4d;
            }
        """)

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

    # ======================================================
    #                       SAVE()
    # ======================================================
    def save(self):

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", self.date.text()):
            QMessageBox.warning(self, "Erreur", "Date invalide (YYYY-MM-DD).")
            return

        data = {
            "id_eleve": self.eleves_map[self.eleve.currentText()],
            "id_personnel": self.personnel_map[self.personnel.currentText()],
            "date_consultation": self.date.text(),
            "type_consultation": self.type.currentText(),
            "symptomes": self.symptomes.text(),
            "diagnostic": self.diagnostic.text(),
            "decisions": self.decision.currentText()
        }

        ok = ConsultationService.update(self.consultation_id, data)

        if ok:
            QMessageBox.information(self, "Succès", "Consultation modifiée.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de mettre à jour.")
