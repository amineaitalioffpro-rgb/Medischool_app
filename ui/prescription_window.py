# ui/prescription_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QInputDialog
)

from PyQt6.QtGui import QColor, QBrush, QFont

from services.prescription_service import PrescriptionService
from services.prescription_medicament_service import PrescriptionMedicamentService

from ui.prescription_form import PrescriptionFormDialog
from ui.prescription_medicament_form import PrescriptionMedicamentFormDialog
from ui.prescription_modify_form import PrescriptionModifyDialog

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class PrescriptionWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ===================== BARRE SUP =====================
        top_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher une prescription…")
        self.search_input.textChanged.connect(self.search)

        btn_refresh = QPushButton("Actualiser")
        btn_add = QPushButton("Ajouter")
        btn_edit = QPushButton("Modifier (ID)")
        btn_delete = QPushButton("Supprimer (ID)")
        btn_add_med = QPushButton("Ajouter Médicament")
        btn_pdf = QPushButton("Imprimer Ordonnance")

        btn_refresh.clicked.connect(self.load_data)
        btn_add.clicked.connect(self.add_prescription)
        btn_edit.clicked.connect(self.modify_prescription_by_id)
        btn_delete.clicked.connect(self.delete_prescription_by_id)
        btn_add_med.clicked.connect(self.add_medicament_to_selected)
        btn_pdf.clicked.connect(self.export_pdf)

        top_bar.addWidget(self.search_input)
        top_bar.addWidget(btn_refresh)
        top_bar.addWidget(btn_add)
        top_bar.addWidget(btn_edit)
        top_bar.addWidget(btn_delete)
        top_bar.addWidget(btn_add_med)
        top_bar.addWidget(btn_pdf)

        layout.addLayout(top_bar)

        # ======================== TABLE ======================
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "ID", "Consultation", "Instructions", "Médicaments"
        ])

        # 🎨 STYLE BEAU + MODERNE
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: white;
                gridline-color: #555;
                font-size: 14px;
                selection-background-color: #444;
            }

            QHeaderView::section {
                background-color: #2e2e2e;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }

            QTableWidget QTableCornerButton::section {
                background-color: #2e2e2e;
            }
        """)

        # Ajustement intelligent des colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)
        self.load_data()

    # ================== CHARGEMENT DONNEES ==================
    def load_data(self):
        rows = PrescriptionService.get_all()
        self.fill_table(rows)

    def fill_table(self, rows):
        self.table.setRowCount(len(rows))

        for i, p in enumerate(rows):

            # ID centré + GRAS
            item_id = QTableWidgetItem(str(p.id_prescription))
            item_id.setTextAlignment(0x0004 | 0x0080)  # center horizontal + vertical
            font = QFont()
            font.setBold(True)
            item_id.setFont(font)
            self.table.setItem(i, 0, item_id)

            # ID consultation (centré)
            item_cons = QTableWidgetItem(str(p.id_consultation))
            item_cons.setTextAlignment(0x0004 | 0x0080)
            self.table.setItem(i, 1, item_cons)

            # Instructions
            self.table.setItem(i, 2, QTableWidgetItem(p.instructions))

            # Liste des médicaments
            meds = PrescriptionMedicamentService.get_by_prescription(p.id_prescription)
            meds_text = ", ".join([m.nom_medicament for m in meds]) or "Aucun"
            self.table.setItem(i, 3, QTableWidgetItem(meds_text))

    # ======================= AJOUT ==========================
    def add_prescription(self):
        dialog = PrescriptionFormDialog(self)
        if dialog.exec():
            self.load_data()

    def add_medicament_to_selected(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Attention", "Sélectionnez une prescription dans la table.")
            return

        id_prescription = int(self.table.item(row, 0).text())
        dialog = PrescriptionMedicamentFormDialog(id_prescription, self)
        if dialog.exec():
            self.load_data()

    # =================== MODIFIER / SUPPRIMER (ID) ==========
    def _ask_id_prescription(self, title: str) -> int | None:
        val, ok = QInputDialog.getInt(
            self, title,
            "ID de la prescription :",
            1, 1, 99999, 1
        )
        return val if ok else None

    def modify_prescription_by_id(self):
        pid = self._ask_id_prescription("Modifier une prescription")
        if pid is None:
            return
        dialog = PrescriptionModifyDialog(pid, self)
        if dialog.exec():
            self.load_data()

    def delete_prescription_by_id(self):
        pid = self._ask_id_prescription("Supprimer une prescription")
        if pid is None:
            return

        confirm = QMessageBox.question(
            self,
            "Confirmation",
            f"Supprimer la prescription #{pid} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        ok = PrescriptionService.delete(pid)
        if ok:
            QMessageBox.information(self, "OK", "Prescription supprimée.")
            self.load_data()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de supprimer la prescription.")

    # ========================= SEARCH =======================
    def search(self):
        text = self.search_input.text().lower().strip()
        if not text:
            self.load_data()
            return

        results = []
        for p in PrescriptionService.get_all():
            meds = PrescriptionMedicamentService.get_by_prescription(p.id_prescription)
            txt_meds = " ".join([m.nom_medicament.lower() for m in meds])

            if (
                text in str(p.id_prescription).lower()
                or text in str(p.id_consultation).lower()
                or text in p.instructions.lower()
                or text in txt_meds
            ):
                results.append(p)

        self.fill_table(results)

    # ======================================================
    #                 EXPORT PDF ORDONNANCE
    # ======================================================
    def export_pdf(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Attention", "Sélectionnez une prescription.")
            return

        id_prescription = int(self.table.item(row, 0).text())
        prescription = PrescriptionService.get_by_id(id_prescription)
        meds = PrescriptionMedicamentService.get_by_prescription(id_prescription)

        file_path = f"ordonnance_{id_prescription}.pdf"

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 60, "ORDONNANCE")

        y = height - 120
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"ID Prescription : {prescription.id_prescription}")
        y -= 20
        c.drawString(50, y, f"ID Consultation : {prescription.id_consultation}")
        y -= 30

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Instructions :")
        y -= 20

        c.setFont("Helvetica", 11)
        for line in prescription.instructions.split("\n"):
            c.drawString(60, y, f"- {line}")
            y -= 18

        y -= 12
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Médicaments :")
        y -= 25

        c.setFont("Helvetica", 11)
        if meds:
            for m in meds:
                c.drawString(60, y, f"- {m.nom_medicament} | {m.dose} | {m.frequence} | {m.duree}")
                y -= 18
        else:
            c.drawString(60, y, "Aucun médicament.")
            y -= 18

        y -= 30
        c.drawString(50, y, "Signature : ________________________")

        c.save()
        QMessageBox.information(self, "PDF", f"PDF généré : {file_path}")
