import pandas as pd


def load_dataset(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def dataset_overview(df: pd.DataFrame) -> dict:
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict()
    }