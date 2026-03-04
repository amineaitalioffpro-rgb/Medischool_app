# ui/prescription_modify_form.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QTextEdit, QPushButton, QHBoxLayout, QMessageBox
)

from services.prescription_service import PrescriptionService


class PrescriptionModifyDialog(QDialog):
    def __init__(self, id_prescription: int, parent=None):
        super().__init__(parent)

        self.id_prescription = id_prescription

        # ================================================
        #                 CONFIG FENÊTRE
        # ================================================
        self.setWindowTitle(f"Modifier Prescription #{id_prescription}")
        self.setFixedSize(420, 330)              # Fenêtre stable et fluide
        self.setStyleSheet("QDialog { background-color: #1b1b1b; color: white; }")

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # ================================================
        #                 CHAMPS DU FORMULAIRE
        # ================================================
        self.id_consultation = QLineEdit()
        self.instructions = QTextEdit()

        # Charger la prescription
        p = PrescriptionService.get_by_id(id_prescription)
        if not p:
            QMessageBox.critical(self, "Erreur", "Prescription introuvable.")
            self.reject()
            return

        self.id_consultation.setText(str(p.id_consultation))
        self.instructions.setText(p.instructions)

        form.addRow("ID Consultation :", self.id_consultation)
        form.addRow("Instructions :", self.instructions)
        layout.addLayout(form)

        # ================================================
        #                    BOUTONS
        # ================================================
        btns = QHBoxLayout()
        btn_save = QPushButton("Mettre à jour")
        btn_cancel = QPushButton("Annuler")

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

        # --- Style professionnel (même vibe que le reste) ---
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #2d79c7;
                color: white;
                padding: 6px 14px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #3c8fe0; }
            QPushButton:pressed { background-color: #1f5c99; }
        """)

        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                padding: 6px 14px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #666; }
            QPushButton:pressed { background-color: #444; }
        """)

        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

    # ================================================
    #                     SAVE()
    # ================================================
    def save(self):

        # Vérification ID consultation
        if not self.id_consultation.text().strip().isdigit():
            QMessageBox.warning(self, "Erreur", "ID consultation invalide.")
            return

        # Vérification instructions
        if not self.instructions.toPlainText().strip():
            QMessageBox.warning(self, "Erreur", "Instructions obligatoires.")
            return

        data = {
            "id_consultation": int(self.id_consultation.text().strip()),
            "instructions": self.instructions.toPlainText().strip()
        }

        # Mise à jour via service
        ok = PrescriptionService.update(self.id_prescription, data)

        if ok:
            QMessageBox.information(self, "OK", "Prescription mise à jour.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de mettre à jour.")
