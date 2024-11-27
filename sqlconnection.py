import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os

import font
import show_table
import excel_page
import db_connections as dc
from option_navigation import streamlit_menu
from typing import Union, List
from pydantic import BaseModel,validator
from st_social_media_links import SocialMediaIcons




social_media_links = [
    "https://www.instagram.com/always_ashrith/",
    "https://www.linkedin.com/in/ladi-asrith-3aa49b248/",
    "https://github.com/Asrith-Ladi",
]

social_media_icons = SocialMediaIcons(social_media_links)
load_dotenv(dotenv_path=r".\.gitignore\.env")
# Pydantic model for query inputs
class MyModel(BaseModel):
    #print("union")
    my_field: Union[str, List[str]]
    
     # Custom validator to ensure that both str and List[str] can be handled
    @validator('my_field', pre=True)
    def normalize_field(cls, v):
        # If it's a list of strings, join them into a single string
        if isinstance(v, list):
            return ', '.join(v)
        #print('v')
        return v  # If it's already a string, just return it

    class Config:
        #print("arbitary")
        arbitrary_types_allowed = True  # Allow arbitrary types if necessary

# Function to get the SQL chain
def get_sql_chain(db: SQLDatabase):
    template = r"""
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.

    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}

    Write only the MSSQL(mandatory) query and nothing else. Do not wrap the MSSQL query in any other text, not even backticks. Please remove any '\_' in the query before execution.
    
    Please reply as restricted, if question related delete, drop, update related query.

    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    Question: Name 10 artists
    SQL Query: SELECT top 10 Name FROM Artist ;

    Your turn:

    Question: {question}
    SQL Query:
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=st.secrets["GROQ"]["api_key"], temperature=0.1)
    
    def get_schema(_):
        #print(db)
        return db.get_table_info()  # Get table schema from the database

    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

# Function to get the response to a user's query
def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    sql_chain = get_sql_chain(db)

    template = r"""
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, MSSQL query, and MSSQL response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>
    Conversation History: {chat_history}

    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=st.secrets["GROQ"]["api_key"], temperature=0)

    chain = (
        RunnablePassthrough.assign(query=sql_chain)
        .assign(schema=lambda _: db.get_table_info())
        .assign(response=lambda vars: db.run(vars["query"].replace('\\_', '_')))  # Replace any escaped underscores
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
    })

# Main function to handle the Streamlit app
def main1():
    # Initialize the chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
        ]
        
    # Setting up Streamlit page components
    font.set_custom_css()
    
    selected = streamlit_menu(2)
    st.title("Chat with Database")
    #st.components.v1.html(font.banner,width=5, height=0)
    # Sidebar setup for Database connection
    if selected == 'Database':
        with st.sidebar:
            social_media_icons.render()
            #google_form_url = "https://forms.gle/i42119tA4YZgdyi27"  # Replace with your Google Form link
            st.markdown(font.feedback_button,
                unsafe_allow_html=True)
            st.subheader("DataBase Details")
            
            # DB credentials and connection logic
            with st.expander("DB Credential Details"):
                creds = st.radio("Do you have RDS DB credentials?", ("Yes", "No"), horizontal=True, key='radio_1')

                if creds == "Yes":
                    db_type = st.selectbox("Select Database Type", options=["MSSQL", "MySQL"], help='Make sure DB should be public and allow relevant port in inbound rule')
                    
                    if db_type == "MSSQL":
                        st.session_state.host = st.text_input("Host", placeholder="your-rds-endpoint")
                        st.session_state.database = st.text_input("Database", placeholder="your_database")
                        st.session_state.user = st.text_input("Username", placeholder="your_username")
                        st.session_state.password = st.text_input("Password", type="password", placeholder="your_password")

                        if st.button("Connect to MSSQL"):
                            if not st.session_state.host or not st.session_state.database or not st.session_state.user or not st.session_state.password:
                                st.error("Please fill in all the fields before connecting!")
                            with st.spinner("Connecting to MSSQL database..."):
                                db = dc.rds_mssql_database(st.session_state.host, st.session_state.database, st.session_state.user, st.session_state.password)
                                if isinstance(db, str):
                                    st.warning(db)
                                else:
                                    st.session_state.db = db
                                    st.session_state.is_connected = True
                                    st.success("Connected to MSSQL database!")
                    elif db_type == "MySQL":
                        st.warning("MySQL support is currently unavailable. Please select MSSQL instead.")
                elif creds == "No":
                    st.markdown('<p class="success-message">Don\'t worry.<br> You can use my credentials by hitting "Connect to Test DataBase"</p>', unsafe_allow_html=True)
                    st.session_state.host = st.secrets["MSSQL"]["host"]
                    st.session_state.database = st.secrets["MSSQL"]["database"]
                    st.session_state.user = st.secrets["MSSQL"]["user"]
                    st.session_state.password = st.secrets["MSSQL"]["password"]
                    if st.button("🌀 Connect to Test DataBase"):
                        with st.spinner("Connecting to MSSQL database..."):
                            db = dc.rds_mssql_database(st.session_state.host, st.session_state.database, st.session_state.user, st.session_state.password)
                            st.toast('Connected!Now test me', icon='😍')
                            st.session_state.db = db
                            st.session_state.is_connected = True
                            st.success("Connected to MSSQL database!")

            if st.session_state.get('is_connected', False):
                #print("sc",st.session_state.host, st.session_state.database, st.session_state.user, st.session_state.password)
                with st.expander("Table Details"):
                    #print("sconnection expander",st.session_state.host, st.session_state.database, st.session_state.user, st.session_state.password)
                    show_table.display_table(st.session_state.host, st.session_state.database, st.session_state.user, st.session_state.password)


    # Handling Excel option (Optional)
    elif selected == "Excel":
        with st.sidebar:
            social_media_icons.render()
            st.markdown(font.feedback_button,unsafe_allow_html=True)
            st.session_state.excel = excel_page.get_excel()

            if st.session_state.excel:
                st.session_state.host = st.secrets["MSSQL"]["host"]
                st.session_state.database = st.secrets["MSSQL"]["db_excel"]
                st.session_state.user = st.secrets["MSSQL"]["user"]
                st.session_state.password = st.secrets["MSSQL"]["password"]
                with st.spinner("Connecting to MSSQL database..."):
                    #print(st.session_state.host, st.session_state.database, st.session_state.user, st.session_state.password)
                    db = dc.rds_mssql_database(st.session_state.host, st.session_state.database, st.session_state.user, st.session_state.password)
                    st.session_state.db = db
                    #print("db",st.session_state.db)
                    #st.session_state.connect_clicked = False
                    st.toast('Connected! Now test me', icon='😍')

    # Display conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
    if "count" not in st.session_state:
        st.session_state.count=0
    # User input for queries
    user_query = st.chat_input("Type a message...")
    if user_query is not None and user_query.strip() != "":
        if st.session_state.count==0:
            st.toast ("Click on Demo button, if you are new to this")
        elif st.session_state.count==3:
            st.toast("We value your thoughts! Please share your feedback with us.")
        elif st.session_state.count==4:
            st.toast ("Please click 'Click me to give feedback' button to share your opiton")
        st.session_state.count+=1
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
            st.markdown(response)

        st.session_state.chat_history.append(AIMessage(content=response))
