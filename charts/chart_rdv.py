# charts/chart_rdv.py

import matplotlib
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from services.statistics_service import StatisticsService


class RendezVousChart(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure(facecolor="#151922")
        super().__init__(self.fig)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#151922")

        self._plot()

    def _plot(self):
        data = StatisticsService.rdv_par_statut()["raw"]
        if not data:
            self.ax.text(0.5, 0.5, "Aucune donnée",
                         ha="center", va="center", color="white")
            return

        labels = [d["statut"] for d in data]
        values = [d["count"] for d in data]

        colors = ["#4da6ff", "#44d17a", "#ff6b6b", "#ffcb4d"]

        self.ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            colors=colors,
            startangle=140,
            textprops={"color": "white"}
        )

        self.ax.set_title("Statut des rendez-vous", color="white", fontsize=13)
