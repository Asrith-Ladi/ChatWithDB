import streamlit as st
from sqlconnection import main1
import show_table as sht
import login as lg
import init_db

st.set_page_config(
        page_title="Chat with Database",
        page_icon=r"Database.png",
        initial_sidebar_state="expanded")

if "db_initialized" not in st.session_state:
    with st.spinner("Initializing databases and tables..."):
        host = st.secrets["MSSQL"]["host"]
        user = st.secrets["MSSQL"]["user"]
        password = st.secrets["MSSQL"]["password"]
        dbs_to_create = [
            st.secrets["MSSQL"]["database"],
            st.secrets["MSSQL"]["db_excel"],
            st.secrets["MSSQL"]["db_login"]
        ]
        if init_db.init_databases_and_tables(host, user, password, dbs_to_create):
            st.session_state.db_initialized = True
        else:
            st.error("Database initialization failed. Please check your credentials and try again.")
            st.stop()

st.session_state.result=False

# Initialize a session state variable to track dialog visibility
if "dialog_open" not in st.session_state:
    st.session_state.dialog_open = True  # Dialog starts as open

# Function to render the dialog box
def popup():
    try:
        st.session_state.result=lg.login_func()
    except Exception as e:
        if'multiple elements with the same' in str(e):
            sht.dialog_box(str(e))
        elif 'database is read-only' in str(e):
            sht.dialog_box("Modification is restricted as it is testing DB")
        else:
            sht.dialog_box("222"+str(e))
    #submit_button = st.button("Submit")  # Submit button to close dialog

    # If submit is clicked, set the dialog to close
    if st.session_state.result:
        st.toast("Thanks for using me!")
        st.session_state.dialog_open = False

# Display the dialog if it's open
if st.session_state.dialog_open:
    popup()
else:
    try:
        main1()
    except Exception as e:
        if 'st.session_state has no attribute "db"' in str(e):
            sht.dialog_box(" Please choose Excel or Database ☝️ fill Credentials on left side bar👈")
        elif 'database is read-only' in str(e):
            sht.dialog_box("Modification is restricted as it is testing DB")
        else:
            sht.dialog_box('111111'+str(e))
            



    