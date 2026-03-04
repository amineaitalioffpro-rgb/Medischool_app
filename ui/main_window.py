# ui/main_window.py

from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from ui.sidebar import Sidebar
from ui.eleves_window import ElevesWindow
from ui.dossiers_window import DossiersWindow
from ui.personnel_window import PersonnelWindow
from ui.consultations_window import ConsultationsWindow
from ui.prescription_window import PrescriptionWindow
from ui.medicament_window import MedicamentWindow
from ui.rendez_vous_window import RendezVousWindow
from ui.vaccination_window import VaccinationWindow
from ui.statistics_window import StatisticsWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MediSchool Manager")
        self.resize(1200, 700)

        # --------------------------
        # CONTENU CENTRAL
        # --------------------------
        central = QWidget()
        self.main_layout = QHBoxLayout(central)
        self.setCentralWidget(central)

        # --------------------------
        # SIDEBAR
        # --------------------------
        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)

        # --------------------------
        # PAGE D’ACCUEIL PAR DÉFAUT
        # --------------------------
        self.content = None
        self._load_welcome()

        # Connexions
        self._connect_sidebar()

    # =====================================================
    # FOND D'ÉCRAN — ACCUEIL
    # =====================================================
    def _load_welcome(self):
        self._clear_content()

        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("background-color: #10141A;")

        pix = QPixmap(
            r"C:\Users\amine\OneDrive\Documents\Projetgest\assets\welcome.png"
        )

        if pix.isNull():
            label.setText("Bienvenue dans MediSchool Manager")
            label.setStyleSheet("font-size: 22px; color: white;")
        else:
            label.setPixmap(
                pix.scaled(
                    900, 500,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

        self.content = label
        self.main_layout.addWidget(self.content)

    # =====================================================
    # NETTOYAGE CONTENU
    # =====================================================
    def _clear_content(self):
        if self.content:
            self.main_layout.removeWidget(self.content)
            self.content.deleteLater()
        self.content = None

    # =====================================================
    # ASSOCIATION DES BOUTONS
    # =====================================================
    def _connect_sidebar(self):

        self.sidebar.buttons["Gestion des Élèves"].clicked.connect(self._load_eleves)
        self.sidebar.buttons["Dossiers Médicaux"].clicked.connect(self._load_dossiers)
        self.sidebar.buttons["Consultations"].clicked.connect(self._load_consultations)
        self.sidebar.buttons["Personnel Médical"].clicked.connect(self._load_personnel)
        self.sidebar.buttons["Prescriptions"].clicked.connect(self._load_prescriptions)
        self.sidebar.buttons["Médicaments"].clicked.connect(self._load_medicaments)
        self.sidebar.buttons["Rendez-vous"].clicked.connect(self._load_rendez_vous)
        self.sidebar.buttons["Vaccinations"].clicked.connect(self._load_vaccinations)
        self.sidebar.buttons["Statistiques & Rapports"].clicked.connect(self._load_stats)

        # ❌ SUPPRIMÉ (car bouton absent)
        # self.sidebar.buttons["Paramètres"].clicked.connect(...)

    # =====================================================
    # AFFICHAGE DES VUES
    # =====================================================
    def _load_eleves(self): self._display(ElevesWindow)
    def _load_dossiers(self): self._display(DossiersWindow)
    def _load_personnel(self): self._display(PersonnelWindow)
    def _load_consultations(self): self._display(ConsultationsWindow)
    def _load_prescriptions(self): self._display(PrescriptionWindow)
    def _load_medicaments(self): self._display(MedicamentWindow)
    def _load_rendez_vous(self): self._display(RendezVousWindow)
    def _load_vaccinations(self): self._display(VaccinationWindow)
    def _load_stats(self): self._display(StatisticsWindow)

    # =====================================================
    # MÉTHODE GÉNÉRIQUE
    # =====================================================
    def _display(self, window_class):
        try:
            self._clear_content()
            widget = window_class()
            self.content = widget
            self.main_layout.addWidget(self.content)

        except Exception as e:
            print(f"❌ ERREUR _display({window_class.__name__}) :", e)
            self._load_label("Erreur lors du chargement")

    # =====================================================
    def _load_label(self, text: str):
        self._clear_content()
        lbl = QLabel(f"Section : {text}")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 22px; color: white;")
        self.content = lbl
        self.main_layout.addWidget(self.content)
