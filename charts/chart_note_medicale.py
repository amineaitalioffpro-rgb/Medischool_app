# charts/chart_note_medicale.py

import matplotlib
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
from services.statistics_service import StatisticsService


class NoteMedicaleGauge(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure(figsize=(3.5, 2.2), facecolor="#151922")
        super().__init__(self.fig)

        self.ax = self.fig.add_subplot(111, polar=True)
        self.ax.set_facecolor("#151922")

        self._plot()

    def _plot(self):
        stats = StatisticsService.note_medicale_stats()
        valeur = stats["avg"]      # moyenne
        min_v = stats["min"]
        max_v = stats["max"]

        # -------------------------
        #  DEMI CERCLE (0 à 10)
        # -------------------------
        theta = np.linspace(0, np.pi, 100)

        self.ax.plot(theta, [1] * 100, color="#4da6ff", linewidth=10, alpha=0.25)

        # Valeur moyenne → angle
        angle = np.pi * (valeur / 10)

        # Pointe bleue
        self.ax.plot([angle], [1], marker="o", markersize=12, color="#4da6ff")

        # Texte affiché
        self.ax.text(
            0, -0.2,
            f"Moyenne : {valeur}/10\nMin : {min_v}   Max : {max_v}",
            ha="center", va="center",
            color="white", fontsize=11
        )

        # Style du gauge
        self.ax.set_ylim(0, 1.05)
        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])
        self.ax.grid(False)
        self.ax.spines["polar"].set_visible(False)
