# ui/dossier_detail.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from services.dossier_service import DossierService

class DossierDetailDialog(QDialog):
    def __init__(self, id_eleve):
        super().__init__()

        self.setWindowTitle("Détails du dossier médical")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        dossier = DossierService.get_by_eleve(id_eleve)

        if dossier is None:
            layout.addWidget(QLabel("Aucun dossier trouvé pour cet élève."))
            return

        layout.addWidget(QLabel(f"ID Élève : {dossier.id_eleve}"))
        layout.addWidget(QLabel(f"Antécédents : {dossier.antecedents}"))
        layout.addWidget(QLabel(f"Allergies : {dossier.allergies}"))
        layout.addWidget(QLabel(f"Note Médicale : {dossier.note_medicale}"))
