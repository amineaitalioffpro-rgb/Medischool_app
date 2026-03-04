# ui/rendez_vous_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QComboBox, QInputDialog
)
from PyQt6.QtGui import QColor, QBrush, QFont
from PyQt6.QtCore import Qt

from services.rendez_vous_service import RendezVousService
from ui.rendez_vous_form import RendezVousFormDialog
from ui.rendez_vous_modify_form import RendezVousModifyDialog

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class RendezVousWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ======================================================
        #                     BARRE SUPÉRIEURE
        # ======================================================
        top_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher : élève, personnel, date, type…")
        self.search_input.textChanged.connect(self.search)

        self.filter_type = QComboBox()
        self.filter_type.addItems(["Tous", "Consultation", "Urgence", "Controle"])
        self.filter_type.currentIndexChanged.connect(self.apply_filters)

        self.filter_statut = QComboBox()
        self.filter_statut.addItems(["Tous", "Planifie", "Confirme", "Annule", "Termine"])
        self.filter_statut.currentIndexChanged.connect(self.apply_filters)

        btn_refresh = QPushButton("Actualiser")
        btn_add = QPushButton("Nouveau RDV")
        btn_modify = QPushButton("Modifier RDV")
        btn_delete = QPushButton("Supprimer")
        btn_pdf = QPushButton("Télécharger PDF")

        btn_refresh.clicked.connect(self.load_data)
        btn_add.clicked.connect(self.add_rdv)
        btn_modify.clicked.connect(self.modify_rdv)
        btn_delete.clicked.connect(self.delete_rdv)
        btn_pdf.clicked.connect(self.export_pdf)

        top_bar.addWidget(self.search_input)
        top_bar.addWidget(self.filter_type)
        top_bar.addWidget(self.filter_statut)
        top_bar.addWidget(btn_refresh)
        top_bar.addWidget(btn_add)
        top_bar.addWidget(btn_modify)
        top_bar.addWidget(btn_delete)
        top_bar.addWidget(btn_pdf)

        layout.addLayout(top_bar)

        # ======================================================
        #                          TABLE
        # ======================================================
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Élève", "Personnel", "Date", "Type", "Statut"
        ])

        # 🎨 Style tableau professionnel
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1b1b1b;
                color: white;
                gridline-color: #444;
                font-size: 14px;
                selection-background-color: #2d79c7;
            }
            QHeaderView::section {
                background-color: #111;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #2d79c7;
                color: black;
            }
        """)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Charger les données
        self.load_data()

    # ======================================================
    #                 CHARGEMENT
    # ======================================================
    def load_data(self):
        self.current_data = RendezVousService.get_all()
        self.fill_table(self.current_data)

    def fill_table(self, rows):
        self.table.setRowCount(len(rows))

        for i, r in enumerate(rows):

            # ID centré et en gras
            id_item = QTableWidgetItem(str(r.id_rdv))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setFont(QFont("Arial", 11, QFont.Weight.Bold))

            self.table.setItem(i, 0, id_item)

            # Colonnes centrées
            elev_item = QTableWidgetItem(r.nom_eleve)
            elev_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 1, elev_item)

            pers_item = QTableWidgetItem(r.nom_personnel)
            pers_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 2, pers_item)

            date_item = QTableWidgetItem(r.date_rdv)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 3, date_item)

            item_type = QTableWidgetItem(r.type_rdv)
            item_type.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            item_statut = QTableWidgetItem(r.statut)
            item_statut.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # 🎨 Couleurs
            self._color_badges(item_type, r.type_rdv)
            self._color_badges(item_statut, r.statut)

            self.table.setItem(i, 4, item_type)
            self.table.setItem(i, 5, item_statut)

    # ======================================================
    #                 COULEURS BADGES
    # ======================================================
    def _color_badges(self, item, value):
        colors = {
            "Urgence": QColor(255, 80, 80),
            "Consultation": QColor(80, 160, 255),
            "Controle": QColor(255, 165, 0),
            "Planifie": QColor(200, 200, 200),
            "Confirme": QColor(70, 200, 120),
            "Annule": QColor(180, 90, 90),
            "Termine": QColor(100, 180, 255),
        }

        if value in colors:
            item.setBackground(QBrush(colors[value]))
            item.setForeground(QBrush(QColor(0, 0, 0)))

    # ======================================================
    #                       RECHERCHE
    # ======================================================
    def search(self):
        text = self.search_input.text().lower()
        results = []

        for r in self.current_data:
            if (
                text in r.nom_eleve.lower()
                or text in r.nom_personnel.lower()
                or text in r.date_rdv.lower()
                or text in r.type_rdv.lower()
                or text in r.statut.lower()
            ):
                results.append(r)

        self.fill_table(results)

    # ======================================================
    #                      FILTRES
    # ======================================================
    def apply_filters(self):
        type_f = self.filter_type.currentText()
        statut_f = self.filter_statut.currentText()

        results = []

        for r in self.current_data:
            if (type_f == "Tous" or r.type_rdv == type_f) and \
               (statut_f == "Tous" or r.statut == statut_f):
                results.append(r)

        self.fill_table(results)

    # ======================================================
    #                      AJOUT RDV
    # ======================================================
    def add_rdv(self):
        dialog = RendezVousFormDialog()
        if dialog.exec():
            self.load_data()

    # ======================================================
    #                     MODIFIER RDV
    # ======================================================
    def modify_rdv(self):
        selected = self.table.currentRow()

        if selected != -1:
            id_rdv = int(self.table.item(selected, 0).text())
        else:
            id_rdv, ok = QInputDialog.getInt(
                self, "Modifier RDV",
                "Entrez l’ID du rendez-vous :",
                1, 1, 999999
            )
            if not ok:
                return

        dialog = RendezVousModifyDialog(id_rdv)

        if dialog.exec():
            self.load_data()

    # ======================================================
    #                     SUPPRIMER RDV
    # ======================================================
    def delete_rdv(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Attention", "Sélectionnez un rendez-vous.")
            return

        id_rdv = int(self.table.item(row, 0).text())

        confirm = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment supprimer ce rendez-vous ?"
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        if RendezVousService.delete(id_rdv):
            QMessageBox.information(self, "Succès", "Rendez-vous supprimé.")
            self.load_data()
        else:
            QMessageBox.critical(self, "Erreur", "La suppression a échoué.")

    # ======================================================
    #                      EXPORT PDF
    # ======================================================
    def export_pdf(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Attention", "Sélectionnez un rendez-vous.")
            return

        id_rdv = int(self.table.item(row, 0).text())
        rdv = RendezVousService.get_by_id(id_rdv)

        file = f"rendez_vous_{id_rdv}.pdf"
        c = canvas.Canvas(file, pagesize=A4)
        w, h = A4

        c.setFont("Helvetica-Bold", 22)
        c.drawString(50, h - 70, "FICHE RENDEZ-VOUS")

        y = h - 130
        c.setFont("Helvetica", 13)

        c.drawString(50, y, f"ID RDV : {rdv.id_rdv}")
        y -= 25
        c.drawString(50, y, f"Élève : {rdv.nom_eleve}")
        y -= 25
        c.drawString(50, y, f"Personnel : {rdv.nom_personnel}")
        y -= 25
        c.drawString(50, y, f"Date : {rdv.date_rdv}")
        y -= 25
        c.drawString(50, y, f"Type : {rdv.type_rdv}")
        y -= 25
        c.drawString(50, y, f"Statut : {rdv.statut}")

        y -= 50
        c.drawString(50, y, "Signature : __________________________")

        c.save()

        QMessageBox.information(self, "PDF généré", f"Fichier créé : {file}")
