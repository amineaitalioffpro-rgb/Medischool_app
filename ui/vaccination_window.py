# ui/vaccination_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QComboBox, QInputDialog
)
from PyQt6.QtGui import QColor, QBrush, QFont
from PyQt6.QtCore import Qt

from services.vaccination_service import VaccinationService
from ui.vaccination_form import VaccinationFormDialog
from ui.vaccination_modify_form import VaccinationModifyDialog

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class VaccinationWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ======================================================
        #                     BARRE SUPÉRIEURE
        # ======================================================
        top_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher : élève, personnel, vaccin, date…")
        self.search_input.textChanged.connect(self.search)

        self.filter_vaccin = QComboBox()
        self.filter_vaccin.addItem("Tous")
        self.filter_vaccin.currentIndexChanged.connect(self.apply_filters)

        self.filter_rappel = QComboBox()
        self.filter_rappel.addItems(["Tous", "OUI", "NON"])
        self.filter_rappel.currentIndexChanged.connect(self.apply_filters)

        btn_refresh = QPushButton("Actualiser")
        btn_add = QPushButton("Nouvelle vaccination")
        btn_modify = QPushButton("Modifier")
        btn_delete = QPushButton("Supprimer")
        btn_pdf = QPushButton("Télécharger PDF")

        btn_refresh.clicked.connect(self.load_data)
        btn_add.clicked.connect(self.add_vaccination)
        btn_modify.clicked.connect(self.modify_vaccination)
        btn_delete.clicked.connect(self.delete_vaccination)
        btn_pdf.clicked.connect(self.export_pdf)

        top_bar.addWidget(self.search_input)
        top_bar.addWidget(self.filter_vaccin)
        top_bar.addWidget(self.filter_rappel)
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
            "ID", "Élève", "Personnel", "Vaccin", "Date", "Rappel"
        ])

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
        self.current_data = VaccinationService.get_all()
        self._update_vaccin_filter()
        self.fill_table(self.current_data)

    def _update_vaccin_filter(self):
        # Mettre à jour la liste des vaccins uniques dans le combo
        current = self.filter_vaccin.currentText() if self.filter_vaccin.count() > 0 else "Tous"
        self.filter_vaccin.blockSignals(True)
        self.filter_vaccin.clear()
        self.filter_vaccin.addItem("Tous")

        vaccins = sorted({v.nom_vaccin for v in self.current_data if v.nom_vaccin})
        for nom in vaccins:
            self.filter_vaccin.addItem(nom)

        # Récupérer la valeur précédente si possible
        index = self.filter_vaccin.findText(current)
        if index != -1:
            self.filter_vaccin.setCurrentIndex(index)
        self.filter_vaccin.blockSignals(False)

    def fill_table(self, rows):
        self.table.setRowCount(len(rows))

        for i, v in enumerate(rows):

            # ID centré et gras
            id_item = QTableWidgetItem(str(v.id_vaccination))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            self.table.setItem(i, 0, id_item)

            elev_item = QTableWidgetItem(v.nom_eleve)
            elev_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 1, elev_item)

            pers_item = QTableWidgetItem(v.nom_personnel)
            pers_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 2, pers_item)

            vaccin_item = QTableWidgetItem(v.nom_vaccin)
            vaccin_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 3, vaccin_item)

            date_item = QTableWidgetItem(v.date_vaccin)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 4, date_item)

            rappel_item = QTableWidgetItem(v.rappel_necessaire)
            rappel_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self._color_badges(rappel_item, v.rappel_necessaire)

            self.table.setItem(i, 5, rappel_item)

    # ======================================================
    #                 COULEURS BADGES
    # ======================================================
    def _color_badges(self, item, value):
        colors = {
            "OUI": QColor(255, 120, 80),
            "NON": QColor(80, 200, 120),
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

        for v in self.current_data:
            if (
                text in v.nom_eleve.lower()
                or text in v.nom_personnel.lower()
                or text in v.nom_vaccin.lower()
                or text in v.date_vaccin.lower()
                or text in v.rappel_necessaire.lower()
            ):
                results.append(v)

        self.fill_table(results)

    # ======================================================
    #                      FILTRES
    # ======================================================
    def apply_filters(self):
        vaccin_f = self.filter_vaccin.currentText()
        rappel_f = self.filter_rappel.currentText()

        results = []

        for v in self.current_data:
            cond_vaccin = (vaccin_f == "Tous" or v.nom_vaccin == vaccin_f)
            cond_rappel = (rappel_f == "Tous" or v.rappel_necessaire == rappel_f)

            if cond_vaccin and cond_rappel:
                results.append(v)

        self.fill_table(results)

    # ======================================================
    #                      AJOUT
    # ======================================================
    def add_vaccination(self):
        dialog = VaccinationFormDialog()
        if dialog.exec():
            self.load_data()

    # ======================================================
    #                     MODIFICATION
    # ======================================================
    def modify_vaccination(self):
        selected = self.table.currentRow()

        if selected != -1:
            id_vaccination = int(self.table.item(selected, 0).text())
        else:
            id_vaccination, ok = QInputDialog.getInt(
                self, "Modifier vaccination",
                "Entrez l’ID de vaccination :",
                1, 1, 999999
            )
            if not ok:
                return

        dialog = VaccinationModifyDialog(id_vaccination)

        if dialog.exec():
            self.load_data()

    # ======================================================
    #                     SUPPRESSION
    # ======================================================
    def delete_vaccination(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Attention", "Sélectionnez une vaccination.")
            return

        id_vaccination = int(self.table.item(row, 0).text())

        confirm = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment supprimer cette vaccination ?"
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        if VaccinationService.delete(id_vaccination):
            QMessageBox.information(self, "Succès", "Vaccination supprimée.")
            self.load_data()
        else:
            QMessageBox.critical(self, "Erreur", "La suppression a échoué.")

    # ======================================================
    #                      EXPORT PDF
    # ======================================================
    def export_pdf(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Attention", "Sélectionnez une vaccination.")
            return

        id_vaccination = int(self.table.item(row, 0).text())
        v = VaccinationService.get_by_id(id_vaccination)

        file = f"vaccination_{id_vaccination}.pdf"
        c = canvas.Canvas(file, pagesize=A4)
        w, h = A4

        c.setFont("Helvetica-Bold", 22)
        c.drawString(50, h - 70, "FICHE VACCINATION")

        y = h - 130
        c.setFont("Helvetica", 13)

        c.drawString(50, y, f"ID Vaccination : {v.id_vaccination}")
        y -= 25
        c.drawString(50, y, f"Élève : {v.nom_eleve}")
        y -= 25
        c.drawString(50, y, f"Personnel : {v.nom_personnel}")
        y -= 25
        c.drawString(50, y, f"Vaccin : {v.nom_vaccin}")
        y -= 25
        c.drawString(50, y, f"Date : {v.date_vaccin}")
        y -= 25
        c.drawString(50, y, f"Rappel nécessaire : {v.rappel_necessaire}")

        y -= 50
        c.drawString(50, y, "Signature : __________________________")

        c.save()

        QMessageBox.information(self, "PDF généré", f"Fichier créé : {file}")
