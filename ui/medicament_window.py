# ui/medicament_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QComboBox
)
from PyQt6.QtGui import QColor, QBrush, QFont
from PyQt6.QtCore import Qt

from services.medicament_service import MedicamentService
from ui.medicament_form import MedicamentFormDialog
from ui.medicament_modify_form import MedicamentModifyDialog


class MedicamentWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ------------------------------------------------------
        #  BARRE SUPÉRIEURE : Recherche + Filtre + Ajouter + Modifier + Supprimer
        # ------------------------------------------------------
        top_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un médicament…")
        self.search_input.textChanged.connect(self.search)

        # --- Filtre effets secondaires ---
        self.filter_cb = QComboBox()
        self.filter_cb.addItems(["Tous", "Aucun", "Avec effets secondaires"])
        self.filter_cb.currentIndexChanged.connect(self.apply_filter)

        btn_add = QPushButton("Ajouter")
        btn_modify = QPushButton("Modifier")
        btn_delete = QPushButton("Supprimer")

        btn_add.clicked.connect(self.add_medicament)
        btn_modify.clicked.connect(self.modify_medicament)
        btn_delete.clicked.connect(self.delete_medicament)

        top_bar.addWidget(self.search_input)
        top_bar.addWidget(self.filter_cb)
        top_bar.addWidget(btn_add)
        top_bar.addWidget(btn_modify)
        top_bar.addWidget(btn_delete)

        layout.addLayout(top_bar)

        # ------------------------------------------------------
        #                      TABLE
        # ------------------------------------------------------
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nom Médicament", "Effets Secondaires"
        ])

        # --- STYLE PRO, MÊME QUE RDV / VACCINATIONS ---
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

        # Charger données
        self.load_data()

    # ------------------------------------------------------
    #                CHARGER DONNÉES
    # ------------------------------------------------------
    def load_data(self):
        rows = MedicamentService.get_all()
        self.fill_table(rows)

    # ------------------------------------------------------
    #     NORMALISATION + AFFICHAGE TABLEAU
    # ------------------------------------------------------
    def fill_table(self, rows):
        self.table.setRowCount(len(rows))
        self.normalized_data = []

        for i, m in enumerate(rows):

            # -------- Normalisation effets secondaires --------
            raw = m.effets_secondaires
            effets = (raw or "").strip()

            if effets == "" or effets.lower() == "aucun":
                category = "aucun"
                display_text = "Aucun"
            else:
                category = "avec"
                display_text = effets

            self.normalized_data.append({
                "id": m.id_medicament,
                "nom": m.nom_medicament,
                "effets": display_text,
                "category": category
            })

            # ID
            item_id = QTableWidgetItem(str(m.id_medicament))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_id.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            self.table.setItem(i, 0, item_id)

            # Nom
            item_nom = QTableWidgetItem(m.nom_medicament)
            item_nom.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 1, item_nom)

            # Effets secondaires (badge)
            item_eff = QTableWidgetItem(display_text)
            item_eff.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if category == "aucun":
                item_eff.setBackground(QBrush(QColor("#8BC34A")))
                item_eff.setForeground(QBrush(QColor(0, 0, 0)))
            else:
                item_eff.setBackground(QBrush(QColor("#FFB74D")))
                item_eff.setForeground(QBrush(QColor(0, 0, 0)))

            self.table.setItem(i, 2, item_eff)

    # ------------------------------------------------------
    #                RECHERCHE
    # ------------------------------------------------------
    def search(self):
        text = self.search_input.text().lower()
        results = []

        for d in self.normalized_data:
            if text in d["nom"].lower() or text in d["effets"].lower():
                results.append(d)

        self.fill_table_from_dict(results)

    # ------------------------------------------------------
    #     AFFICHAGE TABLE TRIÉ (DICT)
    # ------------------------------------------------------
    def fill_table_from_dict(self, rows):
        self.table.setRowCount(len(rows))

        for i, d in enumerate(rows):
            item_id = QTableWidgetItem(str(d["id"]))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, item_id)

            item_nom = QTableWidgetItem(d["nom"])
            item_nom.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 1, item_nom)

            item_eff = QTableWidgetItem(d["effets"])
            item_eff.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if d["category"] == "aucun":
                item_eff.setBackground(QBrush(QColor("#8BC34A")))
            else:
                item_eff.setBackground(QBrush(QColor("#FFB74D")))

            item_eff.setForeground(QBrush(QColor(0, 0, 0)))
            self.table.setItem(i, 2, item_eff)

    # ------------------------------------------------------
    #                FILTRE EFFETS
    # ------------------------------------------------------
    def apply_filter(self):
        choice = self.filter_cb.currentText()
        results = []

        for d in self.normalized_data:
            if choice == "Tous":
                results.append(d)
            elif choice == "Aucun" and d["category"] == "aucun":
                results.append(d)
            elif choice == "Avec effets secondaires" and d["category"] == "avec":
                results.append(d)

        self.fill_table_from_dict(results)

    # ------------------------------------------------------
    #              AJOUT — formulaire pro
    # ------------------------------------------------------
    def add_medicament(self):
        dialog = MedicamentFormDialog(self)
        if dialog.exec():
            self.load_data()

    # ------------------------------------------------------
    #               MODIFICATION — NOUVEAU
    # ------------------------------------------------------
    def modify_medicament(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Attention", "Sélectionnez un médicament.")
            return

        id_medicament = int(self.table.item(row, 0).text())

        dialog = MedicamentModifyDialog(id_medicament, self)
        if dialog.exec():
            self.load_data()

    # ------------------------------------------------------
    #             SUPPRIMER
    # ------------------------------------------------------
    def delete_medicament(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Attention", "Sélectionnez un médicament.")
            return

        id_medicament = int(self.table.item(row, 0).text())

        confirm = QMessageBox.question(
            self, "Supprimer",
            "Supprimer ce médicament ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        if MedicamentService.delete(id_medicament):
            QMessageBox.information(self, "OK", "Médicament supprimé.")
            self.load_data()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de supprimer.")
