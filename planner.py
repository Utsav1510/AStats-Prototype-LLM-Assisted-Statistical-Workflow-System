import json
import re
from ollamafreeapi import OllamaFreeAPI
from utils import infer_variable_type
from prompt import PLANNER_PROMPT


def extract_json_block(text: str) -> str:
    """
    Extract the first JSON object from the raw LLM response text.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0).strip() if match else text.strip()


def normalize_test_name(test_name: str) -> str:
    """
    Normalize different statistical test name variants into supported internal labels.
    """
    if not test_name:
        return ""

    t = test_name.strip().lower()

    mapping = {
        "chi-square test of independence": "chi_square",
        "chi-square test": "chi_square",
        "chi square test": "chi_square",
        "chi square": "chi_square",
        "chi_square": "chi_square",
        "independent t-test": "independent_t_test",
        "independent t test": "independent_t_test",
        "t-test": "independent_t_test",
        "t test": "independent_t_test",
        "independent_t_test": "independent_t_test",
        "anova": "anova",
        "pearson correlation": "pearson_correlation",
        "pearson_correlation": "pearson_correlation",
        "correlation": "pearson_correlation"
    }

    return mapping.get(t, t)


def llm_plan_query(query: str, df_columns: list[str]) -> dict:
    """
    Send the user query and dataset columns to the LLM and return a structured plan.
    """
    client = OllamaFreeAPI()

    prompt = PLANNER_PROMPT.format(
        df_columns=df_columns,
        query=query
    )

    response = client.chat(
        model="gpt-oss:20b",
        prompt=prompt,
        temperature=0
    )

    raw_text = str(response).replace("```json", "").replace("```", "").strip()
    json_text = extract_json_block(raw_text)

    print("\nDEBUG LLM OUTPUT:\n", raw_text)
    print("\nDEBUG JSON BLOCK:\n", json_text)

    try:
        plan = json.loads(json_text)
        if "suggested_test" in plan:
            plan["suggested_test"] = normalize_test_name(plan["suggested_test"])
        return {"success": True, "plan": plan}
    except Exception:
        return {
            "success": False,
            "error": "JSON parsing failed",
            "raw": raw_text
        }


def validate_plan(plan: dict, df):
    """
    Validate the LLM-generated plan against the actual dataset columns and variable types.
    """
    cols = plan.get("candidate_columns", [])

    if len(cols) != 2:
        return {"success": False, "error": "Need exactly 2 columns"}

    actual_columns = list(df.columns)
    corrected_cols = []

    for c in cols:
        match = next((real_col for real_col in actual_columns if real_col.lower() == str(c).lower()), None)
        if match is None:
            return {"success": False, "error": f"{c} not found"}
        corrected_cols.append(match)

    col1, col2 = corrected_cols
    t1 = infer_variable_type(df[col1])
    t2 = infer_variable_type(df[col2])

    if t1 in ["categorical", "binary"] and t2 in ["categorical", "binary"]:
        test = "chi_square"
    elif (t1 in ["categorical", "binary"] and t2 == "numeric") or (t2 in ["categorical", "binary"] and t1 == "numeric"):
        cat = col1 if t1 in ["categorical", "binary"] else col2
        groups = df[cat].dropna().nunique()

        if groups == 2:
            test = "independent_t_test"
        elif groups > 2:
            test = "anova"
        else:
            return {"success": False, "error": "Not enough groups for comparison"}
    elif t1 == "numeric" and t2 == "numeric":
        test = "pearson_correlation"
    else:
        return {"success": False, "error": "Unsupported variable type combination"}

    analysis_goal = plan.get("analysis_goal")
    if not analysis_goal:
        if test == "chi_square":
            analysis_goal = "association_test"
        elif test in ["independent_t_test", "anova"]:
            analysis_goal = "group_comparison"
        else:
            analysis_goal = "correlation_analysis"

    reason = plan.get("reason")
    if not reason:
        reason = f"Validated from data types: {t1}, {t2}"

    return {
        "success": True,
        "plan": {
            "analysis_goal": analysis_goal,
            "candidate_columns": [col1, col2],
            "suggested_test": test,
            "variable_types": {col1: t1, col2: t2},
            "reason": reason
        }
    }


def build_plan(query, df):
    """
    Build the final validated analysis plan for the given user query and dataset.
    """
    llm = llm_plan_query(query, list(df.columns))

    if not llm["success"]:
        return {
            "success": False,
            "error": llm["error"],
            "raw": llm.get("raw", "")
        }

    valid = validate_plan(llm["plan"], df)

    if not valid["success"]:
        return {
            "success": False,
            "error": valid["error"]
        }

    plan = valid["plan"]
    plan["query"] = query

    return {
        "success": True,
        **plan
    }