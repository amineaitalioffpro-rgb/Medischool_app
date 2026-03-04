# charts/chart_vaccins.py

import matplotlib
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from services.statistics_service import StatisticsService


class VaccinsChart(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure(facecolor="#151922")
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)

        self.ax.set_facecolor("#151922")

        self._plot()

    def _plot(self):
        data = StatisticsService.vaccins_par_nom()
        if not data:
            self.ax.text(
                0.5, 0.5,
                "Aucune donnée",
                color="white",
                ha="center", va="center",
                fontsize=12,
                fontweight="bold"
            )
            return

        # Récupération des données
        raw_labels = [d["vaccin"].upper() for d in data]   # MAJUSCULES
        values = [d["count"] for d in data]

        # Transformer en écriture verticale + GRAS
        vertical_labels = ["\n".join(list(label)) for label in raw_labels]

        # --- Bar chart ---
        self.ax.bar(range(len(values)), values, color="#4da6ff")

        # --- Appliquer les labels verticaux ---
        self.ax.set_xticks(range(len(values)))
        self.ax.set_xticklabels(vertical_labels, fontsize=11, fontweight="bold", color="white")

        # --- Titre ---
        self.ax.set_title("Vaccins administrés", color="white", fontsize=13, pad=12)

        # --- Axe Y : seulement entiers ---
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        # --- Style axes ---
        self.ax.spines["bottom"].set_color("#455066")
        self.ax.spines["left"].set_color("#455066")

        for lbl in self.ax.get_yticklabels():
            lbl.set_color("white")
            lbl.set_fontsize(10)
            lbl.set_fontweight("bold")

        # Pour éviter que les labels verticaux soient coupés
        self.fig.subplots_adjust(bottom=0.30)
