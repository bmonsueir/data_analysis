import pandas as pd
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QColor, QBrush, QFont
from PyQt6.QtCore import Qt


def load_csv(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path, na_values=["", " ", "nan", "NaN"])
        df.replace("nan", pd.NA, inplace=True)
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None


def init_column_roles(columns):
    return {col: "Unused" for col in columns}


def populate_table_widget(table_widget: QTableWidget, df: pd.DataFrame, column_roles: dict):
    if df is None or df.empty:
        return

    table_widget.setRowCount(len(df))
    table_widget.setColumnCount(len(df.columns))
    table_widget.setHorizontalHeaderLabels(df.columns)

    for row_idx, row in df.iterrows():
        for col_idx, col in enumerate(df.columns):
            value = row[col]
            item = QTableWidgetItem(str(value))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            role = column_roles.get(col, "Unused")
            font = QFont()
            if role == "Independent":
                font.setBold(True)
                item.setForeground(QBrush(QColor("green")))
            elif role == "Dependent":
                font.setItalic(True)
                item.setForeground(QBrush(QColor("darkred")))
            item.setFont(font)

            table_widget.setItem(row_idx, col_idx, item)


def toggle_column_role(column_name: str, column_roles: dict) -> str:
    current_role = column_roles.get(column_name, "Unused")
    new_role = {
        "Unused": "Independent",
        "Independent": "Dependent",
        "Dependent": "Unused"
    }[current_role]
    column_roles[column_name] = new_role
    return new_role


def extract_variable_roles(column_roles: dict):
    independent_vars = [col for col, role in column_roles.items() if role == "Independent"]
    dependent_vars = [col for col, role in column_roles.items() if role == "Dependent"]
    return independent_vars, dependent_vars


def highlight_data_issues(table_widget: QTableWidget, df: pd.DataFrame):
    df_numeric = df.replace("nan", pd.NA)
    missing_mask = df_numeric.isnull()
    duplicate_mask = df_numeric.duplicated(keep=False)

    for row in range(df_numeric.shape[0]):
        is_dup_row = duplicate_mask.iloc[row]
        for col in range(df_numeric.shape[1]):
            item = table_widget.item(row, col)
            if item is None:
                continue

            is_missing = missing_mask.iloc[row, col]
            if is_missing:
                item.setBackground(QBrush(QColor(255, 255, 0)))  # Yellow for missing
            elif is_dup_row:
                item.setBackground(QBrush(QColor(255, 200, 200)))  # Light red for duplicate row



def clean_data_on_confirmation(table_widget: QTableWidget, df: pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.replace("nan", pd.NA).dropna().drop_duplicates()

    # Clear and reset the table to match cleaned DataFrame
    table_widget.clear()
    table_widget.setRowCount(0)
    table_widget.setColumnCount(0)
    table_widget.setHorizontalHeaderLabels([])

    return df_cleaned

def suggest_data_cleaning(df: pd.DataFrame) -> str:
    messages = []
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        messages.append(f"Found {missing_count} missing values.")
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        messages.append(f"Found {duplicate_count} duplicate rows.")
    return "\n".join(messages) if messages else "No cleaning needed."

def clean_data(df: pd.DataFrame, drop_missing=True, drop_duplicates=True) -> pd.DataFrame:
    if drop_missing:
        df = df.dropna()
    if drop_duplicates:
        df = df.drop_duplicates()
    return df

