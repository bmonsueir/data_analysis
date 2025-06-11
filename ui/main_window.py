from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget,
    QMenuBar, QMenu, QFileDialog, QMessageBox, QPushButton,
    QDockWidget, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QFont

from graphs.plot_generator import PlotWidget
from stats.basic_stats_widget import StatsWidget
from graphs.heat_map import HeatmapWidget
from models.regression_models import RegressionModelWidget
from data_loader import (
    load_csv, init_column_roles, toggle_column_role,
    extract_variable_roles
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = None
        self.problematic_rows = []
        self.column_roles = {}
        self.independent_vars = []
        self.dependent_vars = []
        self.table_widget = QTableWidget()
        

        self.setWindowTitle("Data Analysis App")
        self.setMinimumSize(800, 600)

        self._create_menu_bar()
        self._create_main_layout()

        
        self.table_widget.horizontalHeader().sectionClicked.connect(self._toggle_column_role)

    def _create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        open_action = file_menu.addAction("Open Data File")
        open_action.triggered.connect(self.open_file)

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        view_menu = menubar.addMenu("View")
        plot_action = view_menu.addAction("Show Plot")
        plot_action.triggered.connect(self.show_plot_dock)
        stats_action = view_menu.addAction("Show Statistics")
        stats_action.triggered.connect(self.show_stats_dock)
        heatmap_action = view_menu.addAction("Show Heat Map")
        heatmap_action.triggered.connect(self.show_heatmap_dock)
        regression_action = view_menu.addAction("Show Regression")
        regression_action.triggered.connect(self.show_regression_dock)

        help_menu = menubar.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)

    def _create_main_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _validate_dataframe(self):
        if self.df is None:
            return []
        return self.df[self.df.isnull().any(axis=1) | self.df.duplicated()].index.tolist()

    def _populate_table(self):
        if self.df is None or self.df.empty:
            return

        self.table_widget.setRowCount(len(self.df))
        self.table_widget.setColumnCount(len(self.df.columns) + 1)
        self.table_widget.setHorizontalHeaderLabels(list(self.df.columns) + ["Actions"])

        for row_idx, row in self.df.iterrows():
            is_problematic = row_idx in self.problematic_rows
            for col_idx, col in enumerate(self.df.columns):
                value = row[col]
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                role = self.column_roles.get(col, "Unused")
                font = QFont()
                if role == "Independent":
                    font.setBold(True)
                    item.setForeground(QBrush(QColor("green")))
                elif role == "Dependent":
                    font.setItalic(True)
                    item.setForeground(QBrush(QColor("darkred")))

                if is_problematic:
                    item.setBackground(QBrush(QColor("yellow")))

                item.setFont(font)
                self.table_widget.setItem(row_idx, col_idx, item)

            # Add Remove button in the last column
            if is_problematic:
                remove_btn = QPushButton("Remove")
                remove_btn.clicked.connect(lambda _, r=row_idx: self.remove_row(r))
                self.table_widget.setCellWidget(row_idx, len(self.df.columns), remove_btn)
            else:
                self.table_widget.setCellWidget(row_idx, len(self.df.columns), QWidget())

    def remove_row(self, row_idx):
        if self.df is None or row_idx not in self.df.index:
            return
        self.df = self.df.drop(index=self.df.index[row_idx]).reset_index(drop=True)
        self.problematic_rows = self._validate_dataframe()
        self._populate_table()
        self._update_regression_variables()

    def _clean_data(self):
        if self.df is not None:
            self.df = self.df.dropna().drop_duplicates().reset_index(drop=True)
            self.problematic_rows = self._validate_dataframe()
            self._populate_table()
            self._update_regression_variables()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )
        if file_path:
            df = load_csv(file_path)
            if df is not None:
                self.df = df
                self.column_roles = init_column_roles(self.df.columns)
                self.problematic_rows = self._validate_dataframe()
                self._populate_table()
                self._update_regression_variables()
            else:
                QMessageBox.warning(self, "Error", "Failed to load the CSV file.")

    def _toggle_column_role(self, logicalIndex):
        if self.df is None:
            return
        col_name = self.df.columns[logicalIndex]
        toggle_column_role(col_name, self.column_roles)
        self._populate_table()
        self._update_regression_variables()

    def _update_regression_variables(self):
        self.independent_vars, self.dependent_vars = extract_variable_roles(self.column_roles)
        print("Independent Variables:", self.independent_vars)
        print("Dependent Variables:", self.dependent_vars)

    def show_about(self):
        QMessageBox.about(self, "About", "This is a PyQt6-based Data Analysis App.")

    def show_plot_dock(self):
        if self.df is None or self.df.empty:
            QMessageBox.warning(self, "No Data", "Please load a dataset first.")
            return

        dock = QDockWidget("Data Plot", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        plot_widget = PlotWidget(self.df)
        dock.setWidget(plot_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def show_stats_dock(self):
        if self.df is None or self.df.empty:
            QMessageBox.warning(self, "No Data", "Please load a dataset first.")
            return

        dock = QDockWidget("Basic Statistics", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        stats_widget = StatsWidget(self.df)
        dock.setWidget(stats_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

    def show_heatmap_dock(self):
        if self.df is None or self.df.empty:
            QMessageBox.warning(self, "No Data", "Please load a dataset first.")
            return

        dock = QDockWidget("Heatmap", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        heatmap_widget = HeatmapWidget(self.df)
        dock.setWidget(heatmap_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)

    def show_regression_dock(self):
        if self.df is None or self.df.empty:
            QMessageBox.warning(self, "No Data", "Please load a dataset first.")
            return

        dock = QDockWidget("Regression Model", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        regression_widget = RegressionModelWidget(self.df, self.independent_vars, self.dependent_vars)
        dock.setWidget(regression_widget)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, dock)
