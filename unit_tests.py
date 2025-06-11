import unittest
import pandas as pd

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

class TestDataCleaning(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv("data/pic16b - validate.csv")

    def test_detects_missing_values(self):
        msg = suggest_data_cleaning(self.df)
        self.assertIn("missing", msg.lower(), "Missing values not reported")

    def test_detects_duplicates(self):
        msg = suggest_data_cleaning(self.df)
        self.assertIn("duplicate", msg.lower(), "Duplicates not reported")

    def test_issue_count_matches_data(self):
        expected_missing = self.df.isnull().sum().sum()
        expected_duplicates = self.df.duplicated().sum()
        msg = suggest_data_cleaning(self.df)

        if expected_missing > 0:
            self.assertIn(str(expected_missing), msg, "Incorrect count for missing values")
        if expected_duplicates > 0:
            self.assertIn(str(expected_duplicates), msg, "Incorrect count for duplicate rows")

    def test_clean_missing_only(self):
        cleaned = clean_data(self.df, drop_missing=True, drop_duplicates=False)
        self.assertEqual(cleaned.isnull().sum().sum(), 0)

    def test_clean_duplicates_only(self):
        cleaned = clean_data(self.df, drop_missing=False, drop_duplicates=True)
        self.assertEqual(cleaned.duplicated().sum(), 0)

    def test_clean_both(self):
        cleaned = clean_data(self.df)
        self.assertEqual(cleaned.isnull().sum().sum(), 0)
        self.assertEqual(cleaned.duplicated().sum(), 0)

    def test_idempotent(self):
        first = clean_data(self.df)
        second = clean_data(first)
        pd.testing.assert_frame_equal(first, second)

if __name__ == "__main__":
    unittest.main()
