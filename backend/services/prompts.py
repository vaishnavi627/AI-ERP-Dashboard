# services/prompts.py

def stockout_prediction_prompt(data):
    return f"""
You are an inventory risk prediction AI.

Data:
{data}

Each item includes:
- product name
- current stock
- reorder level
- total units sold

Tasks:
1. Identify products likely to run out within 7 days.
2. Assign risk: High / Medium / Low.
3. Give a short reason.

Return ONLY valid JSON.
"""


def sales_insights_prompt(data):
    return f"""
You are a business intelligence AI.

Sales data:
{data}

Tasks:
1. Identify best-selling products.
2. Identify slow-moving products.
3. Summarize 3 key insights.

Use clear business language.
"""


def reorder_suggestion_prompt(data):
    return f"""
You are a supply chain optimization AI.

Inventory and sales data:
{data}

Tasks:
1. Suggest reorder levels assuming 7-day lead time.
2. Explain each suggestion briefly.

Return JSON only.
"""


def weekly_summary_prompt(weekly_data):
    return f"""
You are an executive reporting AI.

Weekly sales data:
{weekly_data}

Create a concise summary including:
- Revenue
- Units sold
- Trend
- Recommendation

Limit response to 5 bullet points.
"""
