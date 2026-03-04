# ui/consultations_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView,
    QInputDialog, QComboBox
)
from PyQt6.QtGui import QColor, QBrush, QFont
from PyQt6.QtCore import Qt

from services.consultation_service import ConsultationService
from ui.consultation_form import ConsultationFormDialog
from ui.consultation_modify_form import ConsultationModifyDialog

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class ConsultationsWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ======================================================
        #                    BARRE SUPÉRIEURE
        # ======================================================
        top_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher consultation…")
        self.search_input.textChanged.connect(self.apply_filters)

        self.filter_type = QComboBox()
        self.filter_type.addItems(["Tous", "Consultation", "Urgence", "Controle"])
        self.filter_type.currentIndexChanged.connect(self.apply_filters)

        self.filter_decision = QComboBox()
        self.filter_decision.addItems(["Toutes", "Repos", "Traitement", "Transfert"])
        self.filter_decision.currentIndexChanged.connect(self.apply_filters)

        btn_refresh = QPushButton("Actualiser")
        btn_add = QPushButton("Ajouter")
        btn_edit = QPushButton("Modifier")
        btn_delete = QPushButton("Supprimer")
        btn_pdf = QPushButton("PDF")

        btn_refresh.clicked.connect(self.load_data)
        btn_add.clicked.connect(self.add_consultation)
        btn_edit.clicked.connect(self.modify_consultation)
        btn_delete.clicked.connect(self.delete_consultation)
        btn_pdf.clicked.connect(self.export_pdf)

        top_bar.addWidget(self.search_input)
        top_bar.addWidget(self.filter_type)
        top_bar.addWidget(self.filter_decision)
        top_bar.addWidget(btn_refresh)
        top_bar.addWidget(btn_add)
        top_bar.addWidget(btn_edit)
        top_bar.addWidget(btn_delete)
        top_bar.addWidget(btn_pdf)

        layout.addLayout(top_bar)

        # ======================================================
        #                        TABLE
        # ======================================================
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Élève", "Personnel", "Date",
            "Type", "Symptômes", "Diagnostic", "Décision"
        ])

        # pas de numérotation de lignes
        self.table.verticalHeader().setVisible(False)
        # ID plus étroit
        self.table.setColumnWidth(0, 50)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: white;
                gridline-color: #555;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #333;
                color: #eee;
                padding: 6px;
                font-weight: bold;
                border: none;
            }
        """)

        layout.addWidget(self.table)

        self.current_data = []
        self.load_data()

    # ======================================================
    #                 CHARGEMENT DES DONNÉES
    # ======================================================
    def load_data(self):
        self.current_data = ConsultationService.get_all()
        self.apply_filters()

    # ======================================================
    #               REMPLIR LE TABLEAU COMPLET
    # ======================================================
    def fill_table(self, rows):
        self.table.setRowCount(len(rows))

        for i, c in enumerate(rows):

            def add(col, value):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(i, col, item)

            add(0, c.id_consultation)
            add(1, c.nom_eleve)
            add(2, c.nom_personnel)
            add(3, c.date_consultation)

            # TYPE badge
            type_item = QTableWidgetItem(c.type_consultation)
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.apply_type_color(type_item, c.type_consultation)
            self.table.setItem(i, 4, type_item)

            add(5, c.symptomes)
            add(6, c.diagnostic)

            # DECISION badge
            dec_item = QTableWidgetItem(c.decisions)
            dec_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.apply_decision_color(dec_item, c.decisions)
            self.table.setItem(i, 7, dec_item)

    # ======================================================
    #                   COULEUR TYPE
    # ======================================================
    def apply_type_color(self, item, type_c):
        colors = {
            "Urgence": QColor("#ff5050"),
            "Consultation": QColor("#4da6ff"),
            "Controle": QColor("#ffcb4d"),
        }
        if type_c in colors:
            item.setBackground(QBrush(colors[type_c]))
            item.setForeground(QBrush(QColor("black")))
            f = QFont()
            f.setBold(True)
            item.setFont(f)

    # ======================================================
    #                   COULEUR DECISION
    # ======================================================
    def apply_decision_color(self, item, decision):
        colors = {
            "Repos": QColor("#44d17a"),      # vert
            "Traitement": QColor("#ff9f43"), # orange
            "Transfert": QColor("#ff5252"),  # rouge
        }
        if decision in colors:
            item.setBackground(QBrush(colors[decision]))
            item.setForeground(QBrush(QColor("black")))
            f = QFont()
            f.setBold(True)
            item.setFont(f)

    # ======================================================
    #                    AJOUT
    # ======================================================
    def add_consultation(self):
        dialog = ConsultationFormDialog()
        if dialog.exec():
            self.load_data()

    # ======================================================
    #                  ASK ID
    # ======================================================
    def ask_id(self):
        id_text, ok = QInputDialog.getText(self, "Entrer ID", "ID consultation :")
        if not ok or not id_text.isdigit():
            return None
        return int(id_text)

    # ======================================================
    #                    MODIFIER
    # ======================================================
    def modify_consultation(self):
        id_c = self.ask_id()
        if not id_c:
            return
        dialog = ConsultationModifyDialog(id_c)
        if dialog.exec():
            self.load_data()

    # ======================================================
    #                    SUPPRIMER
    # ======================================================
    def delete_consultation(self):
        id_c = self.ask_id()
        if not id_c:
            return

        if ConsultationService.delete(id_c):
            QMessageBox.information(self, "OK", "Consultation supprimée.")
            self.load_data()
        else:
            QMessageBox.critical(self, "Erreur", "Suppression impossible.")

    # ======================================================
    #                    FILTRAGE
    # ======================================================
    def apply_filters(self):
        text = self.search_input.text().lower()
        type_f = self.filter_type.currentText()
        decision_f = self.filter_decision.currentText()

        results = []

        for c in self.current_data:

            ok_type = (type_f == "Tous" or c.type_consultation == type_f)
            ok_decision = (decision_f == "Toutes" or c.decisions == decision_f)

            ok_search = (
                text in c.nom_eleve.lower()
                or text in c.nom_personnel.lower()
                or text in c.type_consultation.lower()
                or text in str(c.date_consultation).lower()
                or text in (c.symptomes or "").lower()
                or text in (c.diagnostic or "").lower()
                or text in (c.decisions or "").lower()
            )

            if ok_type and ok_decision and ok_search:
                results.append(c)

        self.fill_table(results)

    # ======================================================
    #                      PDF EXPORT
    # ======================================================
    def export_pdf(self):
        id_c = self.ask_id()
        if not id_c:
            return

        c = ConsultationService.get_by_id(id_c)
        if not c:
            QMessageBox.warning(self, "Erreur", "Consultation introuvable.")
            return

        file = f"consultation_{id_c}.pdf"
        pdf = canvas.Canvas(file, pagesize=A4)
        w, h = A4

        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(60, h - 60, "FICHE CONSULTATION MÉDICALE")

        pdf.setFont("Helvetica", 12)
        y = h - 110
        space = 24

        fields = [
            ("ID :", c.id_consultation),
            ("Élève :", c.nom_eleve),
            ("Personnel :", c.nom_personnel),
            ("Date :", c.date_consultation),
            ("Type :", c.type_consultation),
            ("Symptômes :", c.symptomes),
            ("Diagnostic :", c.diagnostic),
            ("Décision :", c.decisions),
        ]

        for lbl, val in fields:
            pdf.drawString(60, y, lbl)
            pdf.drawString(180, y, str(val))
            y -= space

        pdf.save()
        QMessageBox.information(self, "PDF généré", f"Fichier : {file}")
