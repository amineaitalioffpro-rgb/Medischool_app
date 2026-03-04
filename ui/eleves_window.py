# ui/eleves_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QComboBox
)
from PyQt6.QtCore import Qt
from services.eleve_service import EleveService
from ui.eleve_form import EleveFormDialog


class ElevesWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ======================================================
        #                     BARRE SUPÉRIEURE
        # ======================================================
        top_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un élève...")
        self.search_input.textChanged.connect(self.apply_filters)

        self.filter_sexe = QComboBox()
        self.filter_sexe.addItems(["Tous", "M", "F"])
        self.filter_sexe.currentIndexChanged.connect(self.apply_filters)

        self.filter_niveau = QComboBox()
        self.filter_niveau.addItems(["Tous"] + [str(i) for i in range(1, 10)])
        self.filter_niveau.currentIndexChanged.connect(self.apply_filters)

        btn_add = QPushButton("Ajouter")
        btn_edit = QPushButton("Modifier")
        btn_delete = QPushButton("Supprimer")

        btn_add.clicked.connect(self.add_eleve)
        btn_edit.clicked.connect(self.edit_selected)
        btn_delete.clicked.connect(self.delete_selected)

        top_bar.addWidget(self.search_input)
        top_bar.addWidget(self.filter_sexe)
        top_bar.addWidget(self.filter_niveau)
        top_bar.addWidget(btn_add)
        top_bar.addWidget(btn_edit)
        top_bar.addWidget(btn_delete)

        layout.addLayout(top_bar)

        # ======================================================
        #                         TABLE
        # ======================================================
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nom", "Prénom", "Date Naissance",
            "Classe", "Sexe", "Groupe Sanguin", "Téléphone Parent"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

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

        layout.addWidget(self.table)

        self.data = []
        self.load_data()

    # ======================================================
    #                     LOAD DATA
    # ======================================================
    def load_data(self):
        self.data = EleveService.get_all()
        self.apply_filters()

    def fill_table(self, rows):
        self.table.setRowCount(len(rows))

        for i, e in enumerate(rows):
            self.table.setItem(i, 0, self.center(str(e.id_eleve)))
            self.table.setItem(i, 1, self.center(e.nom))
            self.table.setItem(i, 2, self.center(e.prenom))
            self.table.setItem(i, 3, self.center(str(e.date_naissance)))
            self.table.setItem(i, 4, self.center(e.classe))
            self.table.setItem(i, 5, self.center(e.sexe))
            self.table.setItem(i, 6, self.center(e.grp_sanguin))
            self.table.setItem(i, 7, self.center(e.telephone_parent))

    def center(self, text):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    # ======================================================
    #                       AJOUT
    # ======================================================
    def add_eleve(self):
        dialog = EleveFormDialog()   # mode ajout
        if dialog.exec():
            self.load_data()

    # ======================================================
    #                       MODIFICATION
    # ======================================================
    def edit_selected(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Attention", "Sélectionnez un élève.")
            return

        id_eleve = int(self.table.item(row, 0).text())

        dialog = EleveFormDialog(id_eleve=id_eleve)  # mode édition
        if dialog.exec():
            self.load_data()

    # ======================================================
    #                   SUPPRESSION
    # ======================================================
    def delete_selected(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Attention", "Sélectionnez un élève.")
            return

        id_eleve = int(self.table.item(row, 0).text())

        if QMessageBox.question(
            self, "Supprimer ?", "Voulez-vous supprimer cet élève ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        ok = EleveService.delete(id_eleve)

        if ok:
            QMessageBox.information(self, "OK", "Élève supprimé.")
            self.load_data()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de supprimer.")

    # ======================================================
    #                   FILTRES
    # ======================================================
    def apply_filters(self):
        text = self.search_input.text().lower()
        sexe_f = self.filter_sexe.currentText()
        niveau_f = self.filter_niveau.currentText()

        results = []

        for e in self.data:
            if (
                text not in e.nom.lower()
                and text not in e.prenom.lower()
                and text not in e.classe.lower()
            ):
                continue

            if sexe_f != "Tous" and e.sexe != sexe_f:
                continue

            niveau_eleve = e.classe[0] if e.classe else ""

            if niveau_f != "Tous" and niveau_eleve != niveau_f:
                continue

            results.append(e)

        self.fill_table(results)
