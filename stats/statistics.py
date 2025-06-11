import pandas as pd

def get_basic_statistics(df):
    """
    Calculate basic statistics for a given pandas DataFrame.

    Parameters:
    - df: pandas.DataFrame, input dataset.

    Returns:
    - dict with statistics: mean, median, std, min, max for numeric columns.
    """
    if df is None or df.empty:
        return {"error": "DataFrame is empty or None."}

    stats = {}
    numeric_df = df.select_dtypes(include=['number'])

    for col in numeric_df.columns:
        stats[col] = {
            "mean": numeric_df[col].mean(),
            "median": numeric_df[col].median(),
            "std": numeric_df[col].std(),
            "min": numeric_df[col].min(),
            "max": numeric_df[col].max(),
        }

    return stats
