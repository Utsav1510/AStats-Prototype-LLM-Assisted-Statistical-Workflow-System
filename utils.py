import pandas as pd


def infer_variable_type(series: pd.Series) -> str:
    """
    Infer the variable type of a pandas Series as categorical, binary, or numeric.
    """
    if pd.api.types.is_numeric_dtype(series):
        unique_count = series.dropna().nunique()
        if unique_count == 2:
            return "binary"
        return "numeric"
    return "categorical"


def clean_pair(df: pd.DataFrame, col1: str, col2: str) -> pd.DataFrame:
    """
    Return a subset of the dataframe with two columns, removing rows with missing values.
    """
    return df[[col1, col2]].dropna()


def normalize_text(text: str) -> str:
    """
    Normalize input text by stripping whitespace and converting to lowercase.
    """
    return text.strip().lower()