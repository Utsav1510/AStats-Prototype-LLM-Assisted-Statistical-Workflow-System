from utils import infer_variable_type, clean_pair


def profile_columns(df, columns):
    """
    Profile the selected dataset columns by identifying variable type,
    missing values, unique values, and either top categorical values
    or summary statistics for numeric data.
    """
    profile = {}

    for col in columns:
        series = df[col]
        profile[col] = {
            "variable_type": infer_variable_type(series),
            "missing_values": int(series.isnull().sum()),
            "unique_values": int(series.nunique(dropna=True))
        }

        if profile[col]["variable_type"] in ["categorical", "binary"]:
            profile[col]["top_values"] = series.value_counts(dropna=True).head(10).to_dict()
        else:
            profile[col]["summary"] = {
                "mean": float(series.dropna().mean()) if not series.dropna().empty else None,
                "std": float(series.dropna().std()) if not series.dropna().empty else None,
                "min": float(series.dropna().min()) if not series.dropna().empty else None,
                "max": float(series.dropna().max()) if not series.dropna().empty else None
            }

    cleaned = clean_pair(df, columns[0], columns[1])

    return {
        "columns": columns,
        "profile": profile,
        "clean_row_count": len(cleaned)
    }