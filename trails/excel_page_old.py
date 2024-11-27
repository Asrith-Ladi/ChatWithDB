import streamlit as st
import pandas as pd
import show_table
import db_connections as dc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData,Column, String, Integer, Float,inspect

engine=dc.mssql_connection("ASHRITH\\sqlexpress","excel_data_storage")


# Function to upload an Excel file to the MySQL database
# Function to upload an Excel file to a specified table in the MS SQL database
def upload_excel_to_db(file, table_name):
    # try:
    #     # Step 1: Create SQLAlchemy engine and session
    #     Session = sessionmaker(bind=engine)
    #     session = Session()

    #     # Step 2: Read Excel file into a pandas DataFrame
    #     df = pd.read_excel(file)
    #     pd.to_sql(df,engine.connect(),index=False, if_exists = 'replace')

    #     # Step 3: Check if the table exists
    #     metadata = MetaData()
    #     # Step 4: Use SQLAlchemy's inspect function to check if the table exists
    #     inspector = inspect(engine)
    #     if table_name not in inspector.get_table_names():
    #         # If the table does not exist, create it dynamically based on DataFrame columns
    #         #columns = {col: String(255) for col in df.columns}
    #         table = Table(table_name, metadata, *[Column(col, String(255)) for col in df.columns], extend_existing=True)
    #         metadata.create_all(engine)  # Create the table in the database

    #     # Step 4: Insert data into the table
    #     # Convert DataFrame to a list of dictionaries (each row is a dictionary)
    #     data = df.to_dict(orient='records')
        
    #     # Perform bulk insert
    #     engine.connect().execute(table.insert(), data)

    #     # Commit and close session
    #     session.commit()
    #     # session.close()

    #     print(f"Data from {file.name} successfully uploaded to {table_name} table.")
    #     return True
    # except Exception as e:
    #     st.toast(f"Error: {str(e)}")
    #     session.rollback()  # Rollback in case of error
    # finally:
    #     session.close()
    df = pd.read_excel(file,na_values=['Not Available','unknown'])
    df.to_sql(table_name,engine.connect(),index=False, if_exists = 'replace')
    return True
    
def get_excel():
    
    # Check if the user is connected to the database
    # if "db" not in st.session_state:
    #     st.error("Please connect to the database first!")
    # else:
    with st.sidebar:
        # Upload Excel file and insert data into DB
        st.subheader("Upload Excel File to Database")
        uploaded_file = st.file_uploader("Choose an Excel file [xlsx]", type=["xlsx"])
        if uploaded_file is not None:
            table_name = st.text_input("Enter table name to store data", value="uploaded_data")
            if st.button("Upload Excel to DB"):
                with st.spinner("Uploading data..."):
                    result=upload_excel_to_db(uploaded_file, table_name)
                    if not result:
                        st.session_state.is_connected = True
                        st.success(f"Data from '{uploaded_file.name}' uploaded successfully to table '{table_name}'.")
            if st.session_state.get('is_connected', False): 
                with st.expander("Table Details"):
                    show_table.display_table()
        
