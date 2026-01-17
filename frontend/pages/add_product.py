import streamlit as st
import requests
API_URL = "http://127.0.0.1:8000"
st.title("Add Product")

if "token" not in st.session_state:
    st.error("Please login first")
    st.stop()
if st.session_state.role != "admin":
    st.error("Only Admin can add products")
    st.stop()
with st.form("add_product_form"):
    name = st.text_input("Product Name")
    stock = st.number_input("Stock Quantity",min_value=0)
    reorder_level = st.number_input("Reorder Level",min_value=0)
    price = st.number_input("Price",min_value=0.0,step=0.1)
    submit = st.form_submit_button("Add Product")
if submit:
    payload = {"name":name,
               "stock":stock,
               "reorder_level":reorder_level,
               "price":price}
    headers = {"Authorization":f"Bearer {st.session_state.token}"}
    response = requests.post(f"{API_URL}/product",json=payload,headers=headers)
    if response.status_code == 200:
            st.success("Product added successfully")
            st.json(response.json())
    else:
            st.error("Failed to add product")