import streamlit as st
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
import pandas as pd
import db_connections as dc
import os
from dotenv import load_dotenv

# Admin credentials
ADMIN_USERNAME = st.secrets["MSSQL"]["admin"]
ADMIN_PASSWORD = st.secrets["MSSQL"]["admin_password"]  # This can be hashed for better security


TABLE = 'users'                 # Your table name

#DATABASE_URL = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
load_dotenv(dotenv_path=".\.gitignore\.env")
# Create SQLAlchemy engine and session
engine = dc.mssql_connection(st.secrets["MSSQL"]["host"],st.secrets["MSSQL"]["db_login"],st.secrets["MSSQL"]["user"],st.secrets["MSSQL"]["password"]).connect()
Session = sessionmaker(bind=engine)
session = Session()

# Function to mask the first 8 characters of a password (for display purposes)
def mask_password(password: str) -> str:
    # Replacing first 8 characters with '*******' and keep the rest of the password intact
    return '*******' + password[8:]

# Function to fetch users data from the MSSQL database
def get_users_data():
    # Define the metadata object to interact with the database
    metadata = MetaData()
    
    # Reflect the 'users' table from the database
    users_table = Table(TABLE, metadata, autoload_with=engine)
    
    # Fetch all rows from the 'users' table
    query = users_table.select()
    result = session.execute(query)
    
    # Convert result to a pandas DataFrame
    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    # Apply the mask function to the 'password' column
    #df['password'] = df['password'].apply(mask_password)
    return df

# Function to display the users' data from the database
def show_users_data():
    st.title("Admin Dashboard")
    st.title("Users Data")
    df = get_users_data()

    # Ensure df is a valid pandas DataFrame
    if isinstance(df, pd.DataFrame):
        st.dataframe(df)
    else:
        st.error("Failed to load user data. Please try again.")

# Streamlit UI
def admin_panel():
    # Check if the user is logged in
    st.title("Admin Login")
    
    username = st.text_input("Username", type="default")
    password = st.text_input("Password", type="password")
    #submit_button = st.form_submit_button("Login")

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.button("Users", on_click=show_users_data)
            
        else:
            st.error("Invalid credentials")
 

# Other admin content can go here (e.g., controls for adding users, etc.)

# Streamlit layout and logic
def main():
    admin_panel()

if __name__ == "__main__":
    main()
