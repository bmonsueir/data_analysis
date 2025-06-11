import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class HeatmapWidget(QWidget):
    def __init__(self, df: pd.DataFrame):
        super().__init__()

        self.df = df
        self.numeric_df = self.df.select_dtypes(include='number')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Dropdown selectors
        self.selector_layout = QHBoxLayout()
        self.row_selector = QComboBox()
        self.col_selector = QComboBox()

        self.row_selector.addItem("(All Rows)")
        self.col_selector.addItem("(All Columns)")

        for col in self.numeric_df.columns:
            self.col_selector.addItem(col)

        self.row_index_map = {}
        for idx in self.numeric_df.index:
            idx_str = str(idx)
            self.row_selector.addItem(idx_str)
            self.row_index_map[idx_str] = idx

        self.row_selector.currentIndexChanged.connect(self.plot_heatmap)
        self.col_selector.currentIndexChanged.connect(self.plot_heatmap)

        self.selector_layout.addWidget(QLabel("Select Row (optional):"))
        self.selector_layout.addWidget(self.row_selector)
        self.selector_layout.addWidget(QLabel("Select Column (optional):"))
        self.selector_layout.addWidget(self.col_selector)
        self.layout.addLayout(self.selector_layout)

        self.canvas = FigureCanvas(plt.Figure(figsize=(10, 6)))
        self.layout.addWidget(self.canvas)

        self.plot_heatmap()

    def plot_heatmap(self):
        if self.numeric_df.empty:
            QMessageBox.warning(self, "No Data", "No numeric data available to generate a heatmap.")
            return

        row_filter = self.row_selector.currentText()
        col_filter = self.col_selector.currentText()

        filtered_df = self.numeric_df

        if row_filter != "(All Rows)":
            try:
                real_index = self.row_index_map[row_filter]
                filtered_df = filtered_df.loc[[real_index]]
            except KeyError:
                QMessageBox.warning(self, "Invalid Row", f"Row '{row_filter}' not found.")
                return

        if col_filter != "(All Columns)":
            filtered_df = filtered_df[[col_filter]]

        self.canvas.figure.clear()
        ax = self.canvas.figure.subplots()

        if filtered_df.empty:
            ax.text(0.5, 0.5, "No numeric data available for heatmap.",
                    ha='center', va='center', transform=ax.transAxes)
        else:
            sns.heatmap(filtered_df, cmap="YlGnBu", ax=ax, annot=True)
            ax.set_title("Heatmap of Selected Data")
            ax.set_xlabel("Columns")
            ax.set_ylabel("Rows")

        self.canvas.draw()
