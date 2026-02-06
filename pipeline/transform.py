"""File to clean the raw data."""

import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file into a DataFrame."""

    return pd.read_csv(file_path)


def save_data(df: pd.DataFrame, file_path: str) -> None:
    """Save DataFrame to a CSV file."""

    df.to_csv(file_path, index=False)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the DataFrame."""

    df = df.dropna()
    df = df.drop_duplicates()
    df["total"] = df["total"].astype(int)

    return df


if __name__ == "__main__":

    data = load_data("./raw_data/FACT_Transaction.csv")

    data = clean_data(data)

    save_data(data, "./clean_data/FACT_Transaction.csv")
