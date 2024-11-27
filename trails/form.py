import streamlit as st

host = st.text_input("Host", placeholder="your-rds-endpoint")
database = st.text_input("Database", placeholder="your_database")
user = st.text_input("Username", placeholder="your_username")
password = st.text_input("Password", type="password", placeholder="your_password")

submit_button = st.form_submit_button("Connect to MSSQL")

if submit_button:
    # Check if any of the fields are empty
    # if not host or not database or not user or not password:
    #     st.error("Please fill in all the fields before connecting!")
    # else:
    with st.spinner("Connecting to MSSQL database..."):
        db = True
        st.session_state.db = db
        st.success("Connected to MSSQL database!")