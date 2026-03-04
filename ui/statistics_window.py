# ui/statistics_window.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QFrame, QGridLayout
from PyQt6.QtCore import Qt

from charts.chart_consultations import ConsultationsChart
from charts.chart_monthly import MonthlyConsultationsChart
from charts.chart_rdv import RendezVousChart
from charts.chart_vaccins import VaccinsChart
from charts.chart_eleves import ElevesCharts
from charts.chart_medical import MedicalCharts

from services.statistics_service import StatisticsService


# ---------------------------------------------------------------
#   MINI CARD
# ---------------------------------------------------------------
class MiniCard(QFrame):
    def __init__(self, title: str, value: str):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #1c212d;
                border-radius: 10px;
                border: 1px solid #2c3442;
            }
            QLabel { color: #dfe6ee; }
            QLabel#cardTitle { font-size: 14px; font-weight: bold; margin-bottom: 4px; }
            QLabel#cardValue { font-size: 13px; }
        """)

        layout = QVBoxLayout(self)
        title_lbl = QLabel(title)
        title_lbl.setObjectName("cardTitle")

        value_lbl = QLabel(value)
        value_lbl.setObjectName("cardValue")
        value_lbl.setWordWrap(True)

        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)


# ---------------------------------------------------------------
#   FENÊTRE PRINCIPALE DES STATISTIQUES
# ---------------------------------------------------------------
class StatisticsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget { background-color: #10141A; color: white; }
            QLabel#titleLabel { font-size: 22px; font-weight: bold; }
            QFrame#card {
                background-color: #151922;
                border-radius: 12px;
                border: 1px solid #262c3a;
            }
            QLabel#cardTitle { font-size: 15px; font-weight: bold; margin-bottom: 4px; }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)

        # ------------------------------------------------
        #   TITRE
        # ------------------------------------------------
        title = QLabel("Statistiques & Rapports — MediSchool Insights")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color:#2b3440; margin-bottom:8px;")
        root.addWidget(line)

        # ------------------------------------------------
        #   TABS
        # ------------------------------------------------
        tabs = QTabWidget()
        root.addWidget(tabs)

        tabs.addTab(self._tab_consultations(), "Consultations")
        tabs.addTab(self._tab_eleves(), "Élèves")
        tabs.addTab(self._tab_medical(), "Activité médicale")
        tabs.addTab(self._tab_rdv_vaccins(), "RDV & Vaccins")

    # ---------------------------------------------------------
    #   CARD HELPER
    # ---------------------------------------------------------
    def _card(self, title=""):
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)

        if title:
            lbl = QLabel(title)
            lbl.setObjectName("cardTitle")
            layout.addWidget(lbl)

        return card, layout

    # ---------------------------------------------------------
    #   ONGLET CONSULTATIONS
    # ---------------------------------------------------------
    def _tab_consultations(self):
        root = QWidget()
        box = QVBoxLayout(root)

        card1, c1 = self._card("Répartition des consultations par type")
        c1.addWidget(ConsultationsChart())
        box.addWidget(card1)

        card2, c2 = self._card("Consultations par mois")
        c2.addWidget(MonthlyConsultationsChart())
        box.addWidget(card2)

        return root

    # ---------------------------------------------------------
    #   ONGLET ÉLÈVES
    # ---------------------------------------------------------
    def _tab_eleves(self):
        root = QWidget()
        layout = QVBoxLayout(root)

        # Graphiques
        card_graph, cg = self._card("Vue d’ensemble des élèves — Graphiques")
        cg.addWidget(ElevesCharts())
        layout.addWidget(card_graph)

        # MiniCards
        notes = StatisticsService.note_medicale_stats()
        allergies = StatisticsService.allergies_principales()

        grid = QGridLayout()
        grid.setSpacing(10)

        note_text = (
            f"<b>Moyenne :</b> {notes['avg']}/10<br>"
            f"<b>Min :</b> {notes['min']}<br>"
            f"<b>Max :</b> {notes['max']}"
        )
        grid.addWidget(MiniCard("Note médicale", note_text), 0, 0)

        if allergies:
            rep_all = ", ".join(f"{a['allergie']} ({a['count']})" for a in allergies[:5])
            grid.addWidget(MiniCard("Top allergies", rep_all), 0, 1)

        layout.addLayout(grid)
        return root

    # ---------------------------------------------------------
    #   ONGLET ACTIVITÉ MÉDICALE
    # ---------------------------------------------------------
    def _tab_medical(self):
        root = QWidget()
        layout = QVBoxLayout(root)

        card_graph, cg = self._card("Graphiques médicaux")
        cg.addWidget(MedicalCharts())
        layout.addWidget(card_graph)

        return root

    # ---------------------------------------------------------
    #   ONGLET RDV + VACCINS (2 colonnes)
    # ---------------------------------------------------------
    def _tab_rdv_vaccins(self):
        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setSpacing(15)

        # Pie chart RDV
        card_rdv, rdv_box = self._card("Statut des rendez-vous")
        rdv_box.addWidget(RendezVousChart())
        layout.addWidget(card_rdv, 1)

        # Vaccins bar chart
        card_vacc, vacc_box = self._card("Vaccinations")
        vacc_box.addWidget(VaccinsChart())
        layout.addWidget(card_vacc, 1)

        return root
