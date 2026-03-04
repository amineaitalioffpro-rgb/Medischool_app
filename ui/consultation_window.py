# ui/consultations_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QFont

from services.consultation_service import ConsultationService
from ui.consultation_form import ConsultationFormDialog


class ConsultationsWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ======================================================
        #                    BARRE SUPÉRIEURE
        # ======================================================
        top_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Rechercher consultation (élève, personnel, date, type, symptomes…)…"
        )
        self.search_input.textChanged.connect(self.search)

        btn_refresh = QPushButton("Actualiser")
        btn_add = QPushButton("Nouvelle Consultation")

        btn_refresh.clicked.connect(self.load_data)
        btn_add.clicked.connect(self.add_consultation)

        top_bar.addWidget(self.search_input)
        top_bar.addWidget(btn_refresh)
        top_bar.addWidget(btn_add)

        layout.addLayout(top_bar)

        # ======================================================
        #                        TABLE
        # ======================================================
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "ID Élève", "ID Personnel",
            "Date", "Type", "Symptômes",
            "Diagnostic", "Décision"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # Style
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #14171d;
                color: white;
                gridline-color: #333;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #1f242c;
                color: white;
                font-weight: bold;
                padding: 6px;
            }
        """)

        layout.addWidget(self.table)

        # stocker les données
        self.current_data = []

        # Charger données
        self.load_data()

    # ======================================================
    #                 CHARGEMENT DES DONNÉES
    # ======================================================
    def load_data(self):
        try:
            self.current_data = ConsultationService.get_all()
            self.fill_table(self.current_data)
        except Exception as e:
            print("❌ ERREUR load_data :", e)
            QMessageBox.critical(self, "Erreur", f"Impossible de charger :\n{e}")

    def fill_table(self, rows):
        self.table.setRowCount(len(rows))

        for i, c in enumerate(rows):

            # ID consultation
            id_item = QTableWidgetItem(str(c.id_consultation))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            self.table.setItem(i, 0, id_item)

            # ID élève
            id_elev = QTableWidgetItem(str(c.id_eleve))
            id_elev.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 1, id_elev)

            # ID personnel
            id_pers = QTableWidgetItem(str(c.id_personnel))
            id_pers.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 2, id_pers)

            # Date
            date_item = QTableWidgetItem(str(c.date_consultation))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 3, date_item)

            # Type
            type_item = QTableWidgetItem(c.type_consultation)
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if c.type_consultation == "Urgence":
                type_item.setBackground(QBrush(QColor("#ff6b6b")))
            elif c.type_consultation == "Controle":
                type_item.setBackground(QBrush(QColor("#ffcb4d")))
            else:
                type_item.setBackground(QBrush(QColor("#4da6ff")))

            type_item.setForeground(QBrush(QColor(0, 0, 0)))
            type_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            self.table.setItem(i, 4, type_item)

            # Symptômes
            sympt_item = QTableWidgetItem(c.symptomes or "")
            sympt_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 5, sympt_item)

            # Diagnostic
            diag_item = QTableWidgetItem(c.diagnostic or "")
            diag_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 6, diag_item)

            # Décision
            dec_item = QTableWidgetItem(c.decisions or "")
            dec_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            dec_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            self.table.setItem(i, 7, dec_item)

    # ======================================================
    #                        AJOUT
    # ======================================================
    def add_consultation(self):
        dialog = ConsultationFormDialog()
        if dialog.exec():
            self.load_data()

    # ======================================================
    #                     RECHERCHE
    # ======================================================
    def search(self):
        text = self.search_input.text().lower().strip()
        if not text:
            self.fill_table(self.current_data)
            return

        results = []
        for c in self.current_data:
            if (
                text in str(c.id_eleve).lower()
                or text in str(c.id_personnel).lower()
                or text in str(c.date_consultation).lower()
                or text in c.type_consultation.lower()
                or text in (c.symptomes or "").lower()
                or text in (c.diagnostic or "").lower()
                or text in (c.decisions or "").lower()
            ):
                results.append(c)

        self.fill_table(results)
