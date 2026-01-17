import streamlit as st
import requests
st.subheader("Add Inventory")

product_id = st.number_input("Product ID", min_value=1)
stock = st.number_input("Stock Quantity", min_value=0)
reorder = st.number_input("Reorder Level", min_value=0)

if st.button("Add Inventory"):
    payload = {
        "product_id": product_id,
        "stock_quantity": stock,
        "reorder_level": reorder
    }

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    response = requests.post(
        "http://127.0.0.1:8000/addinventory",
        json=payload,
        headers=headers
    )

    if response.status_code == 200:
        st.success("Inventory added successfully")
    else:
        st.error("Failed to add inventory")
