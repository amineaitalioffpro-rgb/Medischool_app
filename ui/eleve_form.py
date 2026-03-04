# ui/eleve_form.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QHBoxLayout,
    QMessageBox, QComboBox
)
import re
from services.eleve_service import EleveService


class EleveFormDialog(QDialog):
    def __init__(self, id_eleve=None):
        """
        id_eleve = None  → mode ajout
        id_eleve = int   → mode modification
        """
        super().__init__()

        self.id_eleve = id_eleve
        self.setWindowTitle("Modifier un élève" if id_eleve else "Ajouter un élève")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        form = QFormLayout()
        layout.addLayout(form)

        # ------------------------------
        #       CHAMPS FORMULAIRE
        # ------------------------------
        self.nom = QLineEdit()
        self.prenom = QLineEdit()

        self.date_naissance = QLineEdit()
        self.date_naissance.setPlaceholderText("YYYY-MM-DD")

        self.sexe = QComboBox()
        self.sexe.addItems(["M", "F"])

        self.classe = QComboBox()
        for n in range(1, 10):
            for s in ["A", "B"]:
                self.classe.addItem(f"{n}{s}")

        self.grp_sanguin = QComboBox()
        self.grp_sanguin.addItems(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

        self.telephone_parent = QLineEdit()
        self.telephone_parent.setPlaceholderText("0612345678")

        # --- Ajout au formulaire
        form.addRow("Nom :", self.nom)
        form.addRow("Prénom :", self.prenom)
        form.addRow("Date Naissance :", self.date_naissance)
        form.addRow("Classe :", self.classe)
        form.addRow("Sexe :", self.sexe)
        form.addRow("Groupe sanguin :", self.grp_sanguin)
        form.addRow("Téléphone parent :", self.telephone_parent)

        # ------------------------------
        #       BOUTONS
        # ------------------------------
        btns = QHBoxLayout()
        btn_save = QPushButton("Enregistrer")
        btn_cancel = QPushButton("Annuler")
        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)

        layout.addLayout(btns)

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)

        # ------------------------------
        #   MODE MODIFICATION
        # ------------------------------
        if self.id_eleve:
            self.load_existing()

    # ----------------------------------------------------------
    #        CHARGER ÉLÈVE POUR MODIFICATION
    # ----------------------------------------------------------
    def load_existing(self):
        e = EleveService.get_by_id(self.id_eleve)
        if not e:
            QMessageBox.critical(self, "Erreur", "Élève introuvable.")
            self.reject()
            return

        self.nom.setText(e.nom)
        self.prenom.setText(e.prenom)
        self.date_naissance.setText(str(e.date_naissance))
        self.classe.setCurrentText(e.classe)
        self.sexe.setCurrentText(e.sexe)
        self.grp_sanguin.setCurrentText(e.grp_sanguin)
        self.telephone_parent.setText(e.telephone_parent)

    # ----------------------------------------------------------
    #                         SAVE
    # ----------------------------------------------------------
    def save(self):
        nom = self.nom.text().strip()
        prenom = self.prenom.text().strip()
        date_n = self.date_naissance.text().strip()
        tel = self.telephone_parent.text().strip()

        # VALIDATIONS
        if not nom or not prenom:
            QMessageBox.warning(self, "Erreur", "Nom et prénom obligatoires.")
            return

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_n):
            QMessageBox.warning(self, "Erreur", "Format date incorrect : YYYY-MM-DD")
            return

        if not re.match(r"^0[5-7]\d{8}$", tel):
            QMessageBox.warning(self, "Erreur", "Téléphone invalide (ex : 0612345678).")
            return

        data = {
            "nom": nom,
            "prenom": prenom,
            "date_naissance": date_n,
            "classe": self.classe.currentText(),
            "sexe": self.sexe.currentText(),
            "grp_sanguin": self.grp_sanguin.currentText(),
            "telephone_parent": tel,
        }

        # MODE : AJOUT
        if self.id_eleve is None:
            ok = EleveService.add(data)
        else:
            ok = EleveService.update(self.id_eleve, data)

        if ok:
            QMessageBox.information(self, "OK", "Élève enregistré.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible d’enregistrer l’élève.")
