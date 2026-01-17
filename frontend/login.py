import streamlit as st
import requests
st.title("AI ERP Login")
API_URL="http://127.0.0.1:8000"
if "login" not in st.session_state:
    st.session_state.login = False
name = st.text_input("Enter name")
password = st.text_input("password",type="password")
if st.button("Login"):
    payload = {
        "name":name,
        "password":password
    }
    response = requests.post(f"{API_URL}/login",json=payload)
    if response.status_code == 200:
        data = response.json()
        st.session_state.login = True
        st.session_state.name = data["name"]
        st.session_state.role = data["role"]
        st.session_state.token = data["access_token"]
        st.write("login successfully")
    else:
            st.write("Invalid Credentials")