import streamlit as st
import pandas as pd
import time
from db_connections import mssql_connection
from sqlalchemy import text



@st.dialog(title='Info',width='small')
def dialog_box(msg=""):
    st.warning(msg,icon='⚠️')

@st.dialog(title='Info',width='small')
def table_info(table_selection="",table_data=""):
    st.info(f"**Data from the table: {table_selection}**",icon='📝')
    st.dataframe(table_data)


# Function to fetch the list of tables
def get_table_list(engine):
    query = "SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE'"
    tables = pd.read_sql(query, engine)
    return tables

# def sanitize_table_name(table_name):
#     # Ensure that the table_name is a string and remove non-alphanumeric characters except underscores
#     table_name = str(table_name)
#     if isinstance(table_name, str):
#         table_name = table_name.strip()  # Remove leading/trailing spaces
#         table_name = re.sub(r"[^\w\d_]", "", table_name)  # Remove any non-alphanumeric characters except underscores
#         return table_name
#     else:
#         raise ValueError("The table name should be a string.")

# Function to display the selected table data
def display_table_data(engine,table_name):
   
    # Build the query using the sanitized table name
    query = f"SELECT * FROM {table_name}"
    #print("display")
    # Execute the query and return the result
    df = pd.read_sql(query, engine)
    return df

def display_table(host,database,username,password):
    # Fetch table list from the database
    #print("display_table1",host,database,username,password)

    eng =mssql_connection(host,database,username,password)
    with eng.connect() as engine:
        tables = get_table_list(engine)
        #print("display_table2",tables,host,database,username,password)

        if tables.empty:
            st.error("No tables found in the database.")
        else:
            # Display the table names in a selectbox
            table_names = tables['table_name'].tolist()
            table_selection = st.selectbox("Select a table to view", table_names)

            if table_selection:
                # Fetch the data of the selected table
                with st.spinner(f"Loading data from {table_selection}..."):
                    table_data = display_table_data(engine,table_selection)
                    
                    # Create a dialog-like popup for table display
                    if st.button(f"Show Data for {table_selection}"):
                        
                        bar = st.progress(60)
                        msg = st.toast('Searching Data')
                        msg.toast("weighing the data")
                        time.sleep(3)
                        bar.progress(80)
                        time.sleep(1)
                        msg.toast("Displaying data")
                        bar.progress(100)
                        table_info(table_selection,table_data)
                #engine.dispose()
                
# To test this functionality
#display_table("database-1.ctuq4yyqsjz3.ap-south-1.rds.amazonaws.com","testing","admin","8qCXdHLzExXb5.=-EaC9uGluGSxx%zM&")
                        

