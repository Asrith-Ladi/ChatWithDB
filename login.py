import streamlit as st
import sqlalchemy as sal
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.exc import IntegrityError
import hashlib
import pandas as pd
import db_connections as dc
import os
from dotenv import load_dotenv

import json

import requests  
import streamlit as st  
from streamlit_lottie import st_lottie 

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
    

#lottie_coding = load_lottiefile("lottiefile.json")  # replace link to local lottie file
lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")



def login_func():
    load_dotenv(dotenv_path=r".\.gitignore\.env")
    # print(8)
    # print(os.getenv("MSSQL_HOST"),os.getenv("MSSQL_DB_LOGIN"),os.getenv("MSSQL_USER"),os.getenv("MSSQL_PASSWORD"))
    # Database connection
    engine = dc.mssql_connection(st.secrets["MSSQL"]["host"],st.secrets["MSSQL"]["db_login"],st.secrets["MSSQL"]["user"],st.secrets["MSSQL"]["password"])
    metadata = MetaData()

    # Define the Users table
    users = Table('Users', metadata,
                Column('id', Integer, primary_key=True),
                Column('username', String, unique=True, nullable=False),
                Column('password', String, nullable=False))

    # Create table if it doesn't exist
    metadata.create_all(engine)

    # Function to hash passwords
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    

    # Function to check if a user exists
    def check_user(username, password):
        hashed_password = hash_password(password)
        with engine.connect() as conn:
            result = conn.execute(users.select().where(users.c.username == username, users.c.password == hashed_password)).fetchone()
        return result is not None

    # Function to add a new user
    def add_user(username, password):
        hashed_password = hash_password(password)
        try:
            with engine.connect() as conn:
                conn.execute(users.insert().values({'username': username, 'password': hashed_password}))
                conn.commit()
            return True
        except IntegrityError:
            return False
        
    # Reset password
    def reset_password(username, new_password):
        hashed_password = hash_password(new_password)
        with engine.connect() as conn:
            result = conn.execute(users.update().where(users.c.username == username).values(password=hashed_password))
            conn.commit()
            return result.rowcount > 0
    #bgimage.bg_image('loginbg1.jpg')
    # Streamlit UI
    
    st.title("Let’s connect! Share your details to chat.")

    # Choose between login and signup
    option = st.radio("Choose an option", ["Login", "Signup","Forgot Credentials"],horizontal=True,key='radio_2')

    if option == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if check_user(username, password):
                st.balloons()
                st.success("Login successful! Please hit Login button again")
                return True
            else:
                st.error("Invalid username or password, Please choose Signup or forgot credentials from options")

    elif option == "Signup":
        st.toast("New to this! Please watch demo (available on left sidebar)")
        st.subheader("Signup")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        # Validate password length
        if new_password and len(new_password) < 8:
            st.error("Password must be at least 8 characters long.")

        # Check if passwords match
        if new_password and confirm_password and new_password != confirm_password:
            st.error("Passwords do not match.")

        if st.button("Signup"):
            if len(new_password) >= 8 and new_password == confirm_password:
                if add_user(new_username, new_password):
                    st.success("Signup successful! You can now log in.")
                else:
                    st.error("Username already exists.")
            else:
                st.error("Passwords do not match.")
                
    elif option == "Forgot Credentials":
        st.subheader("Forgot Password")
        username = st.text_input("Enter your username")
        new_password = st.text_input("Enter new password", type="password")
        confirm_password = st.text_input("Confirm new password", type="password")
        
        if st.button("Reset Password"):
            if new_password == confirm_password:
                if reset_password(username, new_password):
                    st.success("Password reset successful! You can now log in with your new password.")
                else:
                    st.error("Username not found.")
            else:
                st.error("Passwords do not match.")
    with st.sidebar:
        st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="low", # medium ; high
        # renderer="svg", # canvas
        height=None,
        width=None,
        key=None,)
        #engine.dispose()
