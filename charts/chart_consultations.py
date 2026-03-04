# charts/chart_consultations.py

import matplotlib
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from services.statistics_service import StatisticsService


class ConsultationsChart(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure(facecolor="#151922")
        super().__init__(self.fig)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#151922")

        self._plot()

    def _plot(self):
        data = StatisticsService.consultations_par_type()
        if not data:
            self.ax.text(0.5, 0.5, "Aucune donnée",
                         color="white", ha="center", va="center")
            return

        labels = [d["type"] for d in data]
        values = [d["count"] for d in data]

        colors = ["#4da6ff", "#ff6b6b", "#ffcb4d"]

        self.ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=140,
            textprops={"color": "white"},
            colors=colors
        )

        
