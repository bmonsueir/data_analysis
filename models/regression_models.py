from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
import pandas as pd

class RegressionModelWidget(QWidget):
    def __init__(self, df, independent_vars, dependent_vars):
        super().__init__()
        self.df = df
        self.independent_vars = independent_vars
        self.dependent_vars = dependent_vars
        self.model = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Select Regression Type:")
        self.layout.addWidget(self.label)

        self.model_selector = QComboBox()
        self.model_selector.addItems(["Linear Regression", "Ridge Regression", "Lasso Regression"])
        self.layout.addWidget(self.model_selector)

        self.run_button = QPushButton("Run Regression")
        self.run_button.clicked.connect(self.run_regression)
        self.layout.addWidget(self.run_button)

        self.result_label = QLabel("Results will appear here.")
        self.result_label.setWordWrap(True)
        self.layout.addWidget(self.result_label)

    def run_regression(self):
        if not self.independent_vars or not self.dependent_vars:
            QMessageBox.warning(self, "Missing Variables", "Please define both independent and dependent variables.")
            return

        X = self.df[self.independent_vars]
        y = self.df[self.dependent_vars[0]]  # Only handle one target for now

        model_type = self.model_selector.currentText()

        if model_type == "Linear Regression":
            self.model = LinearRegression()
        elif model_type == "Ridge Regression":
            self.model = Ridge()
        elif model_type == "Lasso Regression":
            self.model = Lasso()

        self.model.fit(X, y)

        score = self.model.score(X, y)
        coef = self.model.coef_
        intercept = self.model.intercept_

        result = f"R^2 Score: {score:.4f}\nCoefficients: {coef}\nIntercept: {intercept}"
        self.result_label.setText(result)
