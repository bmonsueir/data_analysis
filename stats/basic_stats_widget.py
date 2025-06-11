from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from stats.statistics import get_basic_statistics
import pandas as pd

class StatsWidget(QWidget):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Basic Statistics")
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_area)

        self.display_statistics()

    def display_statistics(self):
        stats = get_basic_statistics(self.df)

        if "error" in stats:
            self.text_area.setText(stats["error"])
        else:
            text = ""
            for col, metrics in stats.items():
                text += f"\n{col} Statistics:\n"
                for key, value in metrics.items():
                    text += f"  {key}: {value:.4f}\n"
            self.text_area.setText(text)
