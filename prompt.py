WELCOME_MESSAGE = """
AStats Prototype (LLM-assisted)

Try queries like:
- Is survival associated with sex?
- Is there a difference in fare between males and females?
- Is fare different across passenger class?
- Is age related to fare?
"""

APPROVAL_PROMPT = "Proceed with this analysis? (yes/no): "

PLANNER_PROMPT = """
You are a statistical workflow planner.

Dataset columns:
{df_columns}

User query:
{query}

Your task:
- identify the two most relevant dataset columns
- choose the appropriate statistical workflow
- choose one supported test name only from:
  chi_square
  independent_t_test
  anova
  pearson_correlation

Rules:
- Return ONLY one JSON object
- Do NOT include markdown
- Do NOT include explanation before or after the JSON
- Use dataset column names exactly as given
- The value of suggested_test must be one of:
  "chi_square", "independent_t_test", "anova", "pearson_correlation"

Return exactly this schema:

{{
  "analysis_goal": "association_test | group_comparison | correlation_analysis",
  "candidate_columns": ["col1", "col2"],
  "suggested_test": "chi_square | independent_t_test | anova | pearson_correlation",
  "reason": "short reason"
}}
"""