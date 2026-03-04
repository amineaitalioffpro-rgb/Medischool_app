# charts/chart_medical.py

import matplotlib
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from services.statistics_service import StatisticsService


class MedicalCharts(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure(facecolor="#151922")
        super().__init__(self.fig)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#151922")

        self._plot()

    def _plot(self):
        data = StatisticsService.top_symptomes()

        if not data:
            self.ax.text(
                0.5, 0.5,
                "Aucune donnée",
                ha="center", va="center",
                color="white", fontsize=12
            )
            return

        # Extraction
        labels = [d["symptome"] for d in data]
        values = [d["count"] for d in data]

        # ------------------------------
        #   BAR CHART VERTICAL
        # ------------------------------
        self.ax.bar(labels, values, color="#4da6ff")

        # Axe X labels
        for lbl in self.ax.get_xticklabels():
            lbl.set_color("white")
            lbl.set_rotation(15)     # légère inclinaison
            lbl.set_fontsize(9)

        # Axe Y labels
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        for lbl in self.ax.get_yticklabels():
            lbl.set_color("white")

        # ------------------------------
        #   STATISTIQUES AVANCÉES
        # ------------------------------
        total = sum(values)
        maxi = max(values)
        sympt_max = labels[values.index(maxi)]
        moyenne = round(total / len(values), 2)

        

        

        # ------------------------------
        #   TITRE
        # ------------------------------
        self.ax.set_title(
            "Symptômes fréquents",
            color="white",
            fontsize=13,
            pad=20
        )
