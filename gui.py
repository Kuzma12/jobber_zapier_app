import streamlit as st
from main import main as run_sync

st.set_page_config(page_title="Jobber Admin Panel", layout="centered")
st.title("Jobber-Zapier Sync Panel")

if st.button("Run Sync Now"):
    try:
        run_sync()
        st.success("✅ Data sync completed successfully!")
    except Exception as e:
        st.error(f"❌ Error occurred during sync: {e}")
