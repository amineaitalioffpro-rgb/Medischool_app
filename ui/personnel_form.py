from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox, QComboBox
)
from services.personnel_service import PersonnelService


class PersonnelFormDialog(QDialog):
    def __init__(self, mode="add", personnel=None):
        super().__init__()

        self.mode = mode      # "add" ou "edit"
        self.personnel = personnel

        self.setWindowTitle("Modifier un membre" if mode == "edit" else "Ajouter un membre")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Champs
        self.nom = QLineEdit()
        self.prenom = QLineEdit()
        self.matricule = QLineEdit()
        self.fonction = QComboBox()
        self.fonction.addItems(["Infirmier", "Medecin", "Assistant", "Secouriste"])
        self.telephone = QLineEdit()

        # Pré-remplissage si EDIT
        if personnel:
            self.nom.setText(personnel.nom)
            self.prenom.setText(personnel.prenom)
            self.matricule.setText(personnel.matricule)
            self.fonction.setCurrentText(personnel.fonction)
            self.telephone.setText(personnel.telephone)

        # Ajout au formulaire
        form.addRow("Nom :", self.nom)
        form.addRow("Prénom :", self.prenom)
        form.addRow("Matricule :", self.matricule)
        form.addRow("Fonction :", self.fonction)
        form.addRow("Téléphone :", self.telephone)

        layout.addLayout(form)

        # Boutons
        btns = QHBoxLayout()
        btn_save = QPushButton("Modifier" if mode == "edit" else "Enregistrer")
        btn_cancel = QPushButton("Annuler")

        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

    # =======================================================
    #                       SAVE
    # =======================================================
    def save(self):

        if not self.nom.text().strip() or not self.prenom.text().strip():
            QMessageBox.warning(self, "Erreur", "Nom/Prénom obligatoires.")
            return

        if len(self.telephone.text().strip()) < 8:
            QMessageBox.warning(self, "Erreur", "Téléphone invalide.")
            return

        data = {
            "nom": self.nom.text().strip(),
            "prenom": self.prenom.text().strip(),
            "matricule": self.matricule.text().strip(),
            "fonction": self.fonction.currentText(),
            "telephone": self.telephone.text().strip()
        }

        if self.mode == "add":
            ok = PersonnelService.add(data)
        else:
            ok = PersonnelService.update(self.personnel.id_personnel, data)

        if ok:
            QMessageBox.information(self, "OK", "Sauvegarde réussie.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible d’enregistrer.")
