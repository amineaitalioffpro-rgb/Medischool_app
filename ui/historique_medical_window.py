# ui/historique_medical_window.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from services.consultation_service import ConsultationService


class HistoriqueMedicalWindow(QDialog):
    def __init__(self, id_eleve: int, nom_eleve: str, parent=None):
        super().__init__(parent)

        self.id_eleve = id_eleve
        self.nom_eleve = nom_eleve

        self.setWindowTitle(f"Historique medical - {nom_eleve}")
        self.resize(800, 400)

        layout = QVBoxLayout(self)

        title = QLabel(f"Historique medical de : {nom_eleve}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Date", "Type", "Personnel", "Symptomes", "Diagnostic"
        ])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        consultations = ConsultationService.get_by_eleve(self.id_eleve)
        self.table.setRowCount(len(consultations))

        for i, c in enumerate(consultations):
            self.table.setItem(i, 0, QTableWidgetItem(str(c.date_consultation)))
            self.table.setItem(i, 1, QTableWidgetItem(c.type_consultation))
            self.table.setItem(i, 2, QTableWidgetItem(c.nom_personnel))
            self.table.setItem(i, 3, QTableWidgetItem(c.symptomes))
            self.table.setItem(i, 4, QTableWidgetItem(c.diagnostic))
