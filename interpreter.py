import pandas as pd


def interpret_result(result, df, plan):
    """
    Generate an interpretation of the statistical result and include
    simple descriptive insights for the selected variables.
    """
    p = result["p"]
    sig = "statistically significant" if p < 0.05 else "not statistically significant"

    c1, c2 = plan["candidate_columns"]

    if result["test"] == "chi_square":
        clean = df[[c1, c2]].dropna()
        table = pd.crosstab(clean[c1], clean[c2])
        proportions = table.div(table.sum(axis=1), axis=0).round(3)

        return (
            f"There is a {sig} association between {c1} and {c2} (p={p:.4f}).\n\n"
            f"Counts:\n{table.to_string()}\n\n"
            f"Row-wise proportions:\n{proportions.to_string()}\n\n"
            f"This shows how the distribution of {c2} differs across categories of {c1}."
        )

    if result["test"] == "independent_t_test":
        clean = df[[c1, c2]].dropna()

        if pd.api.types.is_numeric_dtype(clean[c1]):
            value_col, group_col = c1, c2
        else:
            group_col, value_col = c1, c2

        group_means = clean.groupby(group_col)[value_col].mean().round(3)

        return (
            f"The independent t-test result is {sig} (p={p:.4f}).\n\n"
            f"Group means for {value_col} by {group_col}:\n{group_means.to_string()}\n\n"
            f"This indicates whether the average value of {value_col} differs between the two groups."
        )

    if result["test"] == "anova":
        clean = df[[c1, c2]].dropna()

        if pd.api.types.is_numeric_dtype(clean[c1]):
            value_col, group_col = c1, c2
        else:
            group_col, value_col = c1, c2

        group_means = clean.groupby(group_col)[value_col].mean().round(3)

        return (
            f"The ANOVA result is {sig} (p={p:.4f}).\n\n"
            f"Group means for {value_col} by {group_col}:\n{group_means.to_string()}\n\n"
            f"This indicates whether the average value of {value_col} differs across multiple groups."
        )

    if result["test"] == "pearson_correlation":
        return (
            f"The Pearson correlation result is {sig} (p={p:.4f}).\n\n"
            f"Correlation coefficient: {result['stat']:.4f}\n\n"
            f"This indicates the strength and direction of the linear relationship between {c1} and {c2}."
        )

    return f"{result['test']} result is {sig} (p={p:.4f})"