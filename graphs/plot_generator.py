from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class PlotWidget(QWidget):
    def __init__(self, df):
        super().__init__()

        self.df = df
        self.layout = QVBoxLayout(self)
        
        # Dropdowns
        self.selector_layout = QHBoxLayout()
        self.x_selector = QComboBox()
        self.y_selector = QComboBox()
        self.plot_type_selector = QComboBox()  # <-- Add this line

        for col in df.select_dtypes(include='number').columns:
            self.x_selector.addItem(col)
            self.y_selector.addItem(col)

        self.plot_type_selector.addItems(["Line", "Bar", "Scatter"])  # <-- Add this line

        self.x_selector.currentIndexChanged.connect(self.update_plot)
        self.y_selector.currentIndexChanged.connect(self.update_plot)
        self.plot_type_selector.currentIndexChanged.connect(self.update_plot)  # <-- Add this line

        # Add to layout
        self.selector_layout.addWidget(QLabel("X Axis:"))
        self.selector_layout.addWidget(self.x_selector)
        self.selector_layout.addWidget(QLabel("Y Axis:"))
        self.selector_layout.addWidget(self.y_selector)
        self.selector_layout.addWidget(QLabel("Plot Type:"))  # <-- Add this line
        self.selector_layout.addWidget(self.plot_type_selector)  # <-- Add this line
        self.layout.addLayout(self.selector_layout)

        # Matplotlib Figure
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.update_plot()

    def update_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        x = self.df[self.x_selector.currentText()]
        y = self.df[self.y_selector.currentText()]
        plot_type = self.plot_type_selector.currentText()

        if plot_type == "Line":
            ax.plot(x, y)
        elif plot_type == "Bar":
            ax.bar(x, y)
        elif plot_type == "Scatter":
            ax.scatter(x, y)

        ax.set_xlabel(self.x_selector.currentText())
        ax.set_ylabel(self.y_selector.currentText())
        ax.set_title(f"{plot_type} Plot")

        self.canvas.draw()
