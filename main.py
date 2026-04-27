import streamlit as st
from sqlconnection import main1
import show_table as sht
import login as lg
import init_db
import admin_panel

st.set_page_config(
        page_title="Chat with Database",
        page_icon=r"Database.png",
        initial_sidebar_state="expanded")

# Admin Control Panel always visible in sidebar
with st.sidebar:
    admin_panel.render_admin_panel()
    st.divider()

st.session_state.result = False

# Initialize a session state variable to track dialog visibility
if "dialog_open" not in st.session_state:
    st.session_state.dialog_open = True  # Dialog starts as open

# Function to render the dialog box
def popup():
    try:
        st.session_state.result = lg.login_func()
    except Exception as e:
        err = str(e)
        if 'multiple elements with the same' in err:
            sht.dialog_box(err)
        elif 'database is read-only' in err:
            sht.dialog_box("Modification is restricted as it is testing DB")
        elif 'A network-related or instance-specific error' in err or 'Login timeout expired' in err:
            st.error("Database connection failed. The RDS instance is likely stopped.")
            st.info("👈 Please use the Admin panel in the sidebar to start it.")
        else:
            sht.dialog_box("222" + err)

    # If login is successful, close the popup
    if st.session_state.result:
        st.toast("Thanks for using me!")
        st.session_state.dialog_open = False

# Display the login dialog if not yet logged in
if st.session_state.dialog_open:
    popup()
else:
    try:
        main1()
    except Exception as e:
        err = str(e)
        if 'st.session_state has no attribute "db"' in err:
            sht.dialog_box(" Please choose Excel or Database ☝️ fill Credentials on left side bar👈")
        elif 'database is read-only' in err:
            sht.dialog_box("Modification is restricted as it is testing DB")
        else:
            sht.dialog_box('111111' + err)