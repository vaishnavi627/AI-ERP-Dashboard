# services/ai_service.py

from utils.groq_client import client
from services.ailogic import (
    prepare_inventory_ai_data,
    prepare_sales_ai_data,
    prepare_weekly_sales_data
)
from services.prompts import (
    stockout_prediction_prompt,
    sales_insights_prompt,
    reorder_suggestion_prompt,
    weekly_summary_prompt
)
MODEL_NAME = "llama-3.1-8b-instant"

def generate_stockout_prediction(db):
    """
    Uses Groq LLM to predict which products may run out of stock soon.
    """
    data = prepare_inventory_ai_data(db)
    prompt = stockout_prediction_prompt(data)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

def generate_sales_insights(db):
    """
    Uses Groq LLM to generate business insights from sales data.
    """
    data = prepare_sales_ai_data(db)
    prompt = sales_insights_prompt(data)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content


def generate_reorder_suggestions(db):
    """
    Uses Groq LLM to suggest optimized reorder levels.
    """
    data = prepare_inventory_ai_data(db)
    prompt = reorder_suggestion_prompt(data)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


def generate_weekly_summary(db):
    """
    Uses Groq LLM to summarize last week's performance.
    """
    weekly_data = prepare_weekly_sales_data(db)
    prompt = weekly_summary_prompt(weekly_data)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
