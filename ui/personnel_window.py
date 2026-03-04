# ui/personnel_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
    QComboBox, QHeaderView
)
from PyQt6.QtGui import QColor, QBrush
from services.personnel_service import PersonnelService
from ui.personnel_form import PersonnelFormDialog


class PersonnelWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ======================================================
        #                BARRE SUPÉRIEURE
        # ======================================================
        top_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un membre du personnel…")
        self.search_input.textChanged.connect(self.search)

        # 🔵 FILTRE FONCTION
        self.filter_fonction = QComboBox()
        self.filter_fonction.addItems([
            "Tous", "Medecin", "Infirmier", "Assistant", "Secouriste"
        ])
        self.filter_fonction.currentIndexChanged.connect(self.apply_filters)

        btn_add = QPushButton("Ajouter")
        btn_edit = QPushButton("Modifier")       # <<< AJOUTÉ
        btn_delete = QPushButton("Supprimer")

        btn_add.clicked.connect(self.open_add_dialog)
        btn_edit.clicked.connect(self.open_edit_dialog)     # <<< AJOUTÉ
        btn_delete.clicked.connect(self.delete_selected)

        top_bar.addWidget(self.search_input)
        top_bar.addWidget(self.filter_fonction)
        top_bar.addWidget(btn_add)
        top_bar.addWidget(btn_edit)       # <<< AJOUTÉ
        top_bar.addWidget(btn_delete)

        layout.addLayout(top_bar)

        # ======================================================
        #                     TABLEAU
        # ======================================================
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nom", "Prénom", "Fonction", "Matricule", "Téléphone"
        ])

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: white;
                gridline-color: #444;
                font-size: 14px;
                selection-background-color: #444;
            }
            QHeaderView::section {
                background-color: #333;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.table)

        # Charger données
        self.load_data()

    # ======================================================
    #                 CHARGEMENT DONNÉES
    # ======================================================
    def load_data(self):
        self.data = sorted(
            PersonnelService.get_all(),
            key=lambda p: p.id_personnel
        )
        self.fill_table(self.data)

    def fill_table(self, rows):
        self.table.setRowCount(len(rows))

        for row_idx, p in enumerate(rows):

            # ID
            item_id = QTableWidgetItem(str(p.id_personnel))
            item_id.setTextAlignment(0x0004 | 0x0080)
            self.table.setItem(row_idx, 0, item_id)

            self.table.setItem(row_idx, 1, QTableWidgetItem(p.nom or ""))
            self.table.setItem(row_idx, 2, QTableWidgetItem(p.prenom or ""))

            # Badge couleur fonction
            func_item = QTableWidgetItem(p.fonction)

            if p.fonction == "Medecin":
                color = QColor(70, 200, 255)
            elif p.fonction == "Infirmier":
                color = QColor(255, 165, 0)
            elif p.fonction == "Assistant":
                color = QColor(150, 200, 100)
            elif p.fonction == "Secouriste":
                color = QColor(80, 220, 180)
            else:
                color = QColor(160, 160, 160)

            func_item.setBackground(QBrush(color))
            func_item.setForeground(QBrush(QColor(0, 0, 0)))
            self.table.setItem(row_idx, 3, func_item)

            self.table.setItem(row_idx, 4, QTableWidgetItem(p.matricule or ""))
            self.table.setItem(row_idx, 5, QTableWidgetItem(p.telephone or ""))

    # ======================================================
    #                   RECHERCHE
    # ======================================================
    def search(self):
        text = self.search_input.text().lower()
        results = []

        for p in self.data:
            if (
                text in (p.nom or "").lower()
                or text in (p.prenom or "").lower()
                or text in (p.fonction or "").lower()
                or text in (p.matricule or "").lower()
            ):
                results.append(p)

        self.fill_table(results)

    # ======================================================
    #               FILTRE PAR FONCTION
    # ======================================================
    def apply_filters(self):
        f = self.filter_fonction.currentText()

        if f == "Tous":
            self.fill_table(self.data)
            return

        results = [p for p in self.data if p.fonction == f]
        self.fill_table(results)

    # ======================================================
    #                   AJOUTER
    # ======================================================
    def open_add_dialog(self):
        dialog = PersonnelFormDialog(mode="add")
        if dialog.exec():
            self.load_data()

    # ======================================================
    #                   MODIFIER  <<< AJOUTÉ
    # ======================================================
    def open_edit_dialog(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Attention", "Sélectionnez un personnel à modifier.")
            return

        id_personnel = int(self.table.item(row, 0).text())

        personnel = PersonnelService.get_by_id(id_personnel)

        if not personnel:
            QMessageBox.critical(self, "Erreur", "Impossible de charger ce personnel.")
            return

        dialog = PersonnelFormDialog(mode="edit", personnel=personnel)

        if dialog.exec():
            self.load_data()

    # ======================================================
    #                   SUPPRIMER
    # ======================================================
    def delete_selected(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Attention", "Aucun personnel sélectionné.")
            return

        id_p = int(self.table.item(row, 0).text())

        confirm = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment supprimer ce membre du personnel ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        ok = PersonnelService.delete(id_p)

        if not ok:
            QMessageBox.critical(
                self,
                "Erreur",
                "Impossible de supprimer ce personnel.\nIl est peut-être lié à des consultations."
            )
            return

        QMessageBox.information(self, "OK", "Personnel supprimé.")
        self.load_data()
