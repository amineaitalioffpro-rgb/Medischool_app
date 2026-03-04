# charts/chart_monthly.py

import matplotlib
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from PyQt6.QtWidgets import QMessageBox
from services.statistics_service import StatisticsService


class MonthlyConsultationsChart(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure(facecolor="#151922")
        super().__init__(self.fig)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#151922")

        self.labels = []    # ex: ["2024-12", "2025-01"]
        self.count = []

        self._plot()
        self.mpl_connect("button_press_event", self._on_click)

    def _plot(self):
        data = StatisticsService.consultations_par_mois()

        self.labels = data["labels"]
        self.count = data["count"]

        if not self.labels:
            self.ax.text(0.5, 0.5, "Aucune donnée", color="white",
                         ha="center", va="center")
            return

        # Convertit "2025-01" → "1/25"
        x_labels = []
        x_positions = list(range(len(self.labels)))

        for lab in self.labels:
            year, month = lab.split("-")
            x_labels.append(f"{int(month)}/{year[2:]}")  # ex: 12/24

        # --- COURBE ---
        self.ax.plot(
            x_positions,
            self.count,
            marker="o",
            color="#4da6ff",
            linewidth=2
        )

        # --- Axe X personnalisés ---
        self.ax.set_xticks(x_positions)
        self.ax.set_xticklabels(x_labels, color="white")

        # --- Axe Y = entiers ---
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        # --- Labels axes ---
        self.ax.set_xlabel("Mois", color="white")
        self.ax.set_ylabel("Nombre", color="white")

        # --- Supprimer le titre du chart (car déjà dans la card) ---
        self.ax.set_title("")

        # --- Couleur Y ---
        for label in self.ax.get_yticklabels():
            label.set_color("white")

    # ----------------------------------------------------------------------
    #  Clic sur un point
    # ----------------------------------------------------------------------
    def _on_click(self, event):
        if event.xdata is None:
            return

        # Convertit la position X vers un index réel
        idx = int(round(event.xdata))

        if 0 <= idx < len(self.count):
            mois_affiche = self.labels[idx]  # ex: "2024-12"
            valeur = self.count[idx]

            QMessageBox.information(
                None,
                "Infos",
                f"{mois_affiche} : {valeur} consultations"
            )
