import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind, f_oneway, pearsonr


def execute_plan(plan, df):
    """
    Execute the validated statistical test specified in the plan
    using the selected dataset columns and return the result.
    """
    c1, c2 = plan["candidate_columns"]
    test = plan["suggested_test"]

    clean = df[[c1, c2]].dropna()

    if test == "chi_square":
        table = pd.crosstab(clean[c1], clean[c2])
        stat, p, _, _ = chi2_contingency(table)
        return {"test": test, "stat": stat, "p": p}

    if test == "independent_t_test":
        groups = clean[c1].unique()
        g1 = clean[clean[c1] == groups[0]][c2]
        g2 = clean[clean[c1] == groups[1]][c2]
        stat, p = ttest_ind(g1, g2)
        return {"test": test, "stat": stat, "p": p}

    if test == "anova":
        groups = [g[c2].values for _, g in clean.groupby(c1)]
        stat, p = f_oneway(*groups)
        return {"test": test, "stat": stat, "p": p}

    if test == "pearson_correlation":
        stat, p = pearsonr(clean[c1], clean[c2])
        return {"test": test, "stat": stat, "p": p}