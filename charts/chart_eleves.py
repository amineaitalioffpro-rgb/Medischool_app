# charts/chart_eleves.py

import matplotlib
matplotlib.use("QtAgg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from services.statistics_service import StatisticsService


class ElevesCharts(FigureCanvasQTAgg):
    def __init__(self):
        fig = Figure(figsize=(7, 4), facecolor="#151922")
        super().__init__(fig)

        self.ax1 = fig.add_subplot(131)  # Sexe
        self.ax2 = fig.add_subplot(132)  # Niveaux
        self.ax3 = fig.add_subplot(133)  # Groupes sanguins

        self.fig = fig

        # Espacement global
        fig.subplots_adjust(left=0.05, right=0.97, wspace=0.40)

        # --- décalage léger du Pie Chart ---
        pos1 = self.ax1.get_position()
        self.ax1.set_position([pos1.x0 - 0.03, pos1.y0, pos1.width, pos1.height])

        # --- élargissement LÉGER du graphique des niveaux ---
        pos2 = self.ax2.get_position()
        self.ax2.set_position([
            pos2.x0 - 0.04,      # petit décalage
            pos2.y0,
            pos2.width + 0.05,   # petite augmentation
            pos2.height
        ])

        self._plot()

    def _plot(self):

        # ======================================================
        # SEXE — Pie Chart
        # ======================================================
        data = StatisticsService.eleves_par_sexe()
        labels = ["M", "F"]
        values = [data["M"], data["F"]]

        self.ax1.set_facecolor("#151922")
        self.ax1.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            colors=["#4da6ff", "#ff7999"],
            textprops={"color": "white"}
        )
        self.ax1.set_title("Sexe", color="white")

        # ======================================================
        # NIVEAUX TRIES
        # ======================================================
        classes = StatisticsService.eleves_par_classe()
        if classes:
            niveaux = {}
            for c in classes:
                niveau = ''.join(ch for ch in c["classe"] if ch.isdigit())
                if niveau:
                    niveaux[niveau] = niveaux.get(niveau, 0) + c["count"]

            # tri
            niveaux = dict(sorted(niveaux.items(), key=lambda x: int(x[0])))

            labels = list(niveaux.keys())
            values = list(niveaux.values())

            self.ax2.set_facecolor("#151922")
            self.ax2.bar(labels, values, color="#4da6ff")

            self.ax2.set_title("Niveaux", color="white")
            self.ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

            for lbl in self.ax2.get_xticklabels():
                lbl.set_color("white")
            for lbl in self.ax2.get_yticklabels():
                lbl.set_color("white")

        # ======================================================
        # Groupes sanguins
        # ======================================================
        groupes = StatisticsService.eleves_par_groupe_sanguin()
        if groupes:
            labels = [g["groupe"] for g in groupes]
            values = [g["count"] for g in groupes]

            self.ax3.set_facecolor("#151922")
            self.ax3.barh(labels, values, color="#8e44ad")

            self.ax3.set_title("Groupes sanguins", color="white")
            self.ax3.xaxis.set_major_locator(MaxNLocator(integer=True))

            for lbl in self.ax3.get_yticklabels():
                lbl.set_color("white")
            for lbl in self.ax3.get_xticklabels():
                lbl.set_color("white")
