# ui/dashboard_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

import pyqtgraph as pg

from services.statistics_service import StatisticsService


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MediSchool Manager - Dashboard")
        self.setMinimumSize(900, 600)

        # ---- Couleurs globales (style dark + bleu néon) ----
        self.setStyleSheet("""
            QWidget {
                background-color: #111219;
                color: #f5f5f5;
            }
            QLabel#titleLabel {
                color: #4da3ff;
                font-weight: bold;
                letter-spacing: 2px;
            }
            QLabel#sectionLabel {
                color: #cccccc;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ==========================
        #       TITRE TOP
        # ==========================
        title = QLabel("MEDISCHOOL - DASHBOARD ANALYTICS")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))

        subtitle = QLabel("Vue globale des consultations, élèves et vaccinations")
        subtitle.setObjectName("sectionLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        subtitle.setFont(QFont("Segoe UI", 10))

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # ==========================
        #       GRAPHIQUES
        # ==========================
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        top_layout.setSpacing(20)
        bottom_layout.setSpacing(20)

        # --------- Graph 1 : Consultations par mois ---------
        self.consult_month_plot = pg.PlotWidget()
        self._style_plot_widget(self.consult_month_plot, "Consultations par mois")
        top_layout.addWidget(self.consult_month_plot)

        # --------- Graph 2 : Consultations par type ---------
        self.consult_type_plot = pg.PlotWidget()
        self._style_plot_widget(self.consult_type_plot, "Consultations par type")
        top_layout.addWidget(self.consult_type_plot)

        # --------- Graph 3 : Répartition sexe ---------
        self.sexe_plot = pg.PlotWidget()
        self._style_plot_widget(self.sexe_plot, "Répartition des élèves par sexe")
        bottom_layout.addWidget(self.sexe_plot)

        # --------- Graph 4 : Vaccinations rappel ---------
        self.vaccin_plot = pg.PlotWidget()
        self._style_plot_widget(self.vaccin_plot, "Vaccinations : rappel nécessaire")
        bottom_layout.addWidget(self.vaccin_plot)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        # Charger les données
        self.load_data()

    # ==========================
    #  Méthode utilitaire style
    # ==========================
    def _style_plot_widget(self, widget: pg.PlotWidget, title: str):
        widget.setBackground("#111219")
        widget.showGrid(x=True, y=True, alpha=0.15)
        widget.setTitle(
            title,
            color="#4da3ff",
            size="12pt"
        )
        # Axes en bleu léger
        axis_pen = pg.mkPen("#4da3ff")
        widget.getAxis("left").setPen(axis_pen)
        widget.getAxis("bottom").setPen(axis_pen)
        widget.getAxis("left").setTextPen("#dddddd")
        widget.getAxis("bottom").setTextPen("#dddddd")

    # ==========================
    #      LOAD DATA
    # ==========================
    def load_data(self):
        self._load_consultations_by_month()
        self._load_consultations_by_type()
        self._load_sexe_distribution()
        self._load_vaccination_rappel()

    # ----- Graphique : consultations par mois -----
    def _load_consultations_by_month(self):
        labels, values = StatisticsService.get_consultations_by_month()
        self.consult_month_plot.clear()

        if not labels:
            return

        x = list(range(len(labels)))

        curve = self.consult_month_plot.plot(
            x, values,
            pen=pg.mkPen("#4da3ff", width=2),
            symbol="o",
            symbolSize=8,
            symbolBrush="#4da3ff"
        )
        self.consult_month_plot.getPlotItem().getAxis("bottom").setTicks([list(zip(x, labels))])
        self.consult_month_plot.setLabel("left", "Nombre de consultations")
        self.consult_month_plot.setLabel("bottom", "Mois")

    # ----- Graphique : consultations par type -----
    def _load_consultations_by_type(self):
        labels, values = StatisticsService.get_consultations_by_type()
        self.consult_type_plot.clear()

        if not labels:
            return

        x = list(range(len(labels)))
        bg = pg.BarGraphItem(x=x, height=values, width=0.6, brush="#2979ff")
        self.consult_type_plot.addItem(bg)
        self.consult_type_plot.getPlotItem().getAxis("bottom").setTicks([list(zip(x, labels))])
        self.consult_type_plot.setLabel("left", "Nombre de consultations")
        self.consult_type_plot.setLabel("bottom", "Type")

    # ----- Graphique : répartition des sexes -----
    def _load_sexe_distribution(self):
        labels, values = StatisticsService.get_sexe_distribution()
        self.sexe_plot.clear()

        if not labels:
            return

        x = list(range(len(labels)))
        bg = pg.BarGraphItem(x=x, height=values, width=0.6, brush="#00e5ff")
        self.sexe_plot.addItem(bg)
        self.sexe_plot.getPlotItem().getAxis("bottom").setTicks([list(zip(x, labels))])
        self.sexe_plot.setLabel("left", "Nombre d'élèves")
        self.sexe_plot.setLabel("bottom", "Sexe")

    # ----- Graphique : vaccinations rappel -----
    def _load_vaccination_rappel(self):
        labels, values = StatisticsService.get_vaccination_rappel_distribution()
        self.vaccin_plot.clear()

        if not labels:
            return

        x = list(range(len(labels)))
        bg = pg.BarGraphItem(x=x, height=values, width=0.6, brush="#00c853")
        self.vaccin_plot.addItem(bg)
        self.vaccin_plot.getPlotItem().getAxis("bottom").setTicks([list(zip(x, labels))])
        self.vaccin_plot.setLabel("left", "Nombre de vaccinations")
        self.vaccin_plot.setLabel("bottom", "Rappel")
