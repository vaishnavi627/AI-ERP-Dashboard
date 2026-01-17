import streamlit as st
import requests
import pandas as pd
import json

API_URL = "http://127.0.0.1:8000"


if not st.session_state.get("login"):
    st.warning("Please login first")
    st.stop()

st.title("📊 Admin Dashboard")

headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}


inventory_res = requests.get(f"{API_URL}/getinventory", headers=headers)
inventory_df = pd.DataFrame(inventory_res.json())

st.subheader("🏬 Inventory Stock")
st.dataframe(inventory_df)

st.bar_chart(
    inventory_df.set_index("product_id")["stock_quantity"]
)

# ---------------- SALES ----------------
sales_res = requests.get(f"{API_URL}/sales", headers=headers)
sales_df = pd.DataFrame(sales_res.json())

sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"])

st.subheader("💰 Sales Data")
st.dataframe(sales_df)

# 📈 Revenue trend
st.subheader("📈 Revenue Over Time")
revenue_chart = sales_df.groupby("sale_date")["revenue"].sum()
st.line_chart(revenue_chart)

# 🛒 Quantity sold per product
st.subheader("🛒 Quantity Sold per Product")
quantity_chart = sales_df.groupby("product_id")["quantity_sold"].sum()
st.bar_chart(quantity_chart)

# ---------------- LOW STOCK ALERT ----------------
st.subheader("⚠️ Low Stock Alert")
low_stock = inventory_df[
    inventory_df["stock_quantity"] <= inventory_df["reorder_level"]
]

if low_stock.empty:
    st.success("All products are sufficiently stocked 🎉")
else:
    st.warning("Products need restocking!")
    st.dataframe(low_stock)

st.title("🤖 AI-Powered ERP Dashboard")

# ===============================
# 1️⃣ STOCK-OUT PREDICTION
# ===============================
st.subheader("⚠️ Stock Run-Out Prediction")

if st.button("Predict Stock Risk"):
    res = requests.get(
        f"{API_URL}/predict-stockout",
        headers=headers
    )

    if res.status_code == 200:
        ai_result = res.json()["data"]

        try:
            stock_df = json.loads(ai_result)
            st.dataframe(stock_df)
        except:
            st.write(ai_result)
    else:
        st.error("Failed to fetch stock prediction")


# ===============================
# 2️⃣ SALES INSIGHTS
# ===============================
st.subheader("📈 AI Sales Insights")

if st.button("Generate Sales Insights"):
    res = requests.get(
        f"{API_URL}/sales-insights",
        headers=headers
    )

    if res.status_code == 200:
        st.success(res.json()["data"])
    else:
        st.error("Failed to fetch sales insights")


# ===============================
# 3️⃣ REORDER SUGGESTIONS
# ===============================
st.subheader("🔁 Reorder Level Suggestions")

if st.button("Suggest Reorder Levels"):
    res = requests.get(
        f"{API_URL}/reorder-suggestions",
        headers=headers
    )

    if res.status_code == 200:
        ai_result = res.json()["data"]

        try:
            reorder_df = json.loads(ai_result)
            st.dataframe(reorder_df)
        except:
            st.write(ai_result)
    else:
        st.error("Failed to fetch reorder suggestions")


# ===============================
# 4️⃣ WEEKLY SUMMARY
# ===============================
st.subheader("🗓️ Last Week Performance Summary")

if st.button("Generate Weekly Summary"):
    res = requests.get(
        f"{API_URL}/weekly-summary",
        headers=headers
    )

    if res.status_code == 200:
        st.info(res.json()["data"])
    else:
        st.error("Failed to fetch weekly summary")
