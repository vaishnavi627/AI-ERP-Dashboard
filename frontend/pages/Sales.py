import streamlit as st
import requests
import pandas as pd

if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state:
    st.session_state.role = None

API_URL = "http://127.0.0.1:8000"

headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}

st.title("📈 Sales")

# Upload CSV (Admin only)
if st.session_state.role == "admin":
    file = st.file_uploader("Upload Sales CSV", type=["csv"])

    if file and st.button("Upload"):
        files = {
            "file": (file.name, file.getvalue(), "text/csv")
        }

        response = requests.post(
            f"{API_URL}/upload",
            headers=headers,
            files=files
        )

        if response.status_code == 200:
            st.success(response.json().get("message", "Sales uploaded successfully"))
        else:
            st.error(response.text)

# View sales
response = requests.get(f"{API_URL}/sales", headers=headers)

if response.status_code != 200:
    st.error(response.text)
    st.stop()

data = response.json()

if not isinstance(data, list):
    st.error("Invalid sales data returned from API")
    st.write(data)
    st.stop()

df = pd.DataFrame(data)

if df.empty:
    st.info("No sales data available")
else:
    st.dataframe(df)
