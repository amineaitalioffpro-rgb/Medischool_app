# ui/dossiers_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget,
    QTableWidgetItem, QPushButton, QComboBox, QHeaderView, QMessageBox
)
from PyQt6.QtGui import QColor, QBrush

from services.dossier_service import DossierService
from ui.dossier_detail import DossierDetailDialog
from ui.dossier_add_dialog import DossierAddDialog


class DossiersWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ======================================================
        #                     BARRE SUPÉRIEURE
        # ======================================================
        top_bar = QHBoxLayout()

        # --- BOUTON AJOUTER ---
        btn_add = QPushButton("➕ Ajouter")
        btn_add.setStyleSheet(
            "background-color:#2d8cff; padding:6px 12px; border-radius:6px; color:white;"
        )
        btn_add.clicked.connect(self.add_dossier)
        top_bar.addWidget(btn_add)

        # --- Barre de recherche ---
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un dossier médical...")
        self.search_input.textChanged.connect(self.search)
        top_bar.addWidget(self.search_input)

        # --- FILTRE ALLERGIE ---
        self.filter_allergie = QComboBox()
        self.filter_allergie.addItems(["Tous", "Avec allergie", "Sans allergie"])
        self.filter_allergie.currentIndexChanged.connect(self.apply_filters)
        top_bar.addWidget(self.filter_allergie)

        # --- FILTRE NOTE ---
        self.filter_note = QComboBox()
        self.filter_note.addItems([
            "Toutes les notes",
            "Note > 7 (Vert)",
            "5 ≤ Note ≤ 7 (Orange)",
            "Note < 5 (Rouge)"
        ])
        self.filter_note.currentIndexChanged.connect(self.apply_filters)
        top_bar.addWidget(self.filter_note)

        layout.addLayout(top_bar)

        # ======================================================
        #                       TABLEAU
        # ======================================================
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID Dossier", "Élève", "Antécédents", "Allergies", "Note", "Action", "Supprimer"
        ])

        # ---- STYLE PRO ----
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: white;
                gridline-color: #444;
                font-size: 14px;
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
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        self.table.verticalHeader().setDefaultSectionSize(38)

        layout.addWidget(self.table)

        # Charger données
        self.load_data()

    # ======================================================
    #                CHARGER DONNÉES
    # ======================================================
    def load_data(self):
        self.data = DossierService.get_all()
        self.fill_table(self.data)

    def fill_table(self, rows):
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):

            # ID
            self.table.setItem(i, 0, QTableWidgetItem(str(row["id_dossier"])))

            # Élève
            self.table.setItem(i, 1, QTableWidgetItem(f'{row["nom"]} {row["prenom"]}'))

            # Antécédents
            self.table.setItem(i, 2, QTableWidgetItem(row["antecedents"] or ""))

            # Allergies
            self.table.setItem(i, 3, QTableWidgetItem(row["allergies"] or ""))

            # NOTE + COULEUR
            note = row["note_medicale"] if row["note_medicale"] is not None else 0
            note_item = QTableWidgetItem(str(note))
            self.apply_note_color(note_item, note)
            self.table.setItem(i, 4, note_item)

            # BOUTON VOIR
            btn_view = QPushButton("Voir")
            btn_view.clicked.connect(lambda _, id=row["id_eleve"]: self.open_detail(id))
            self.table.setCellWidget(i, 5, btn_view)

            # BOUTON SUPPRIMER
            btn_del = QPushButton("Supprimer")
            btn_del.setStyleSheet("background-color:#c62828; color:white; padding:4px;")
            btn_del.clicked.connect(lambda _, id=row["id_dossier"]: self.delete_dossier(id))
            self.table.setCellWidget(i, 6, btn_del)

    # ======================================================
    #            COULEURS SELON LA NOTE
    # ======================================================
    def apply_note_color(self, item, note):

        if note > 7:
            color = QColor(70, 200, 120)  # Vert
        elif 5 <= note <= 7:
            color = QColor(255, 165, 0)   # Orange
        else:
            color = QColor(255, 80, 80)   # Rouge

        item.setBackground(QBrush(color))
        item.setForeground(QBrush(QColor(0, 0, 0)))

    # ======================================================
    #                     RECHERCHE
    # ======================================================
    def search(self):
        text = self.search_input.text().lower()
        results = []

        for row in self.data:
            if (
                text in row["nom"].lower()
                or text in row["prenom"].lower()
                or text in (row["antecedents"] or "").lower()
                or text in (row["allergies"] or "").lower()
            ):
                results.append(row)

        self.fill_table(results)

    # ======================================================
    #                   FILTRES AVANCÉS
    # ======================================================
    def apply_filters(self):
        allergie_f = self.filter_allergie.currentText()
        note_f = self.filter_note.currentText()

        results = []

        for row in self.data:

            # Allergies
            has_allergie = (row["allergies"] or "").strip().lower() not in ["", "aucune"]

            if allergie_f == "Avec allergie" and not has_allergie:
                continue
            if allergie_f == "Sans allergie" and has_allergie:
                continue

            # Notes
            note = row["note_medicale"] or 0

            if note_f == "Note > 7 (Vert)" and not (note > 7):
                continue
            if note_f == "5 ≤ Note ≤ 7 (Orange)" and not (5 <= note <= 7):
                continue
            if note_f == "Note < 5 (Rouge)" and not (note < 5):
                continue

            results.append(row)

        self.fill_table(results)

    # ======================================================
    #          OUVERTURE DÉTAIL DOSSIER
    # ======================================================
    def open_detail(self, id_eleve):
        dialog = DossierDetailDialog(id_eleve)
        dialog.exec()

    # ======================================================
    #          SUPPRIMER DOSSIER
    # ======================================================
    def delete_dossier(self, id_dossier):
        confirm = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment supprimer ce dossier ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            if DossierService.delete(id_dossier):
                QMessageBox.information(self, "OK", "Dossier supprimé.")
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de supprimer le dossier.")
            self.load_data()

    # ======================================================
    #          AJOUTER DOSSIER
    # ======================================================
    def add_dossier(self):
        dialog = DossierAddDialog()
        if dialog.exec():
            self.load_data()
