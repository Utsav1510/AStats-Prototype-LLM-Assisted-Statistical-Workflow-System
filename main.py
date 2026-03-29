from data import load_dataset, dataset_overview
from prompt import WELCOME_MESSAGE, APPROVAL_PROMPT
from planner import build_plan
from profiler import profile_columns
from stats_engine import execute_plan
from interpreter import interpret_result


def print_overview(info: dict):
    """
    Print basic dataset information including shape and column names.
    """
    print("\nDataset overview")
    print(f"Shape: {info['shape']}")
    print(f"Columns: {info['columns']}")


def print_plan(plan: dict):
    """
    Display the generated analysis plan including query, selected columns,
    variable types, chosen statistical test, and reasoning.
    """
    print("\nSuggested analysis plan")
    print(f"Query: {plan['query']}")
    print(f"Analysis goal: {plan['analysis_goal']}")
    print(f"Columns: {plan['candidate_columns']}")
    print(f"Variable types: {plan['variable_types']}")
    print(f"Suggested test: {plan['suggested_test']}")
    print(f"Reason: {plan['reason']}")


def print_profile(profile: dict):
    """
    Print profiling details for selected columns including type, missing values,
    unique values, and summary statistics or top categorical values.
    """
    print("\nProfile summary")
    print(f"Clean rows available: {profile['clean_row_count']}")

    for col, info in profile["profile"].items():
        print(f"\nColumn: {col}")
        print(f"Type: {info['variable_type']}")
        print(f"Missing values: {info['missing_values']}")
        print(f"Unique values: {info['unique_values']}")

        if "top_values" in info:
            print(f"Top values: {info['top_values']}")

        if "summary" in info:
            print(f"Summary: {info['summary']}")


def main():
    """
    Execute the end-to-end workflow:
    - Load dataset
    - Accept user query
    - Generate and validate analysis plan
    - Profile selected variables
    - Get user approval
    - Run statistical test
    - Display results and interpretation
    """
    df = load_dataset("./data/titanic.csv")
    info = dataset_overview(df)

    print(WELCOME_MESSAGE)
    print_overview(info)

    query = input("\nEnter your analysis question: ").strip()

    plan = build_plan(query, df)

    if not plan["success"]:
        print(f"\nCould not build plan: {plan['error']}")
        if "raw" in plan and plan["raw"]:
            print("\nRaw LLM output:")
            print(plan["raw"])
        return

    print_plan(plan)

    profile = profile_columns(df, plan["candidate_columns"])
    print_profile(profile)

    approval = input(f"\n{APPROVAL_PROMPT}").strip().lower()

    if approval != "yes":
        print("\nAnalysis stopped by user.")
        return

    result = execute_plan(plan, df)
    interpretation = interpret_result(result, df, plan)

    print("\nStatistical result")
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nInterpretation")
    print(interpretation)


if __name__ == "__main__":
    main()