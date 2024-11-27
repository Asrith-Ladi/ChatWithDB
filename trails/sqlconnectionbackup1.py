from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

import streamlit as st
import font
import show_table
from option_navigation import streamlit_menu
import excel_page
import db_connections as dc



def main1():
    
    def get_sql_chain(db):
        template = """
        You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.

        <SCHEMA>{schema}</SCHEMA>

        Conversation History: {chat_history}

        Write only the MSSQL query and nothing else. Do not wrap the MSSQL query in any other text, not even backticks. Please remove any '\_' in the query before execution.

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
        llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key="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", temperature=0)

        def get_schema(_):
            #st.write(db.get_table_info())
            return db.get_table_info()
        st.write(db.get_table_info())
        return (
            RunnablePassthrough.assign(schema=get_schema)
            | prompt
            | llm
            | StrOutputParser()
        )

    def get_response(user_query: str, db: SQLDatabase, chat_history: list):
        sql_chain = get_sql_chain(db)

        template = """
        You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, question, MSSQL query, and MSSQL response, write a natural language response.
        <SCHEMA>{schema}</SCHEMA>

        Conversation History: {chat_history}

        SQL Query: <SQL>{query}</SQL>

        User question: {question}
        SQL Response: {response}
        """

        prompt = ChatPromptTemplate.from_template(template)
        llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key="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", temperature=0)

        chain = (
            RunnablePassthrough.assign(query=sql_chain).assign(
                schema=lambda _: db.get_table_info(),
                response=lambda vars: db.run(vars["query"].replace('\\_', '_'))
            )
            | prompt
            | llm
            | StrOutputParser()
        )

        return chain.invoke({
            "question": user_query,
            "chat_history": chat_history,
        })

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
        ]

    load_dotenv()

    # Setting up Streamlit
    
    
    font.set_custom_css()
    selected = streamlit_menu(2)
    st.title("Chat with Database")
    # if "excel" not in st.session_state:
    #     st.session_state.excel= False
    #     st.write( st.session_state.excel)
        
    if selected=='Database':
        # Sidebar setup for MSSQL RDS configuration
        with st.sidebar:

            st.subheader("DataBase Details")
            
            with st.expander("DB Credential Details"):
                creds = st.radio("Do you have RDS DB credentials?", ("Yes", "No"), horizontal=True,help='Click no for testing',key='radio_1')
                
                if creds=="Yes":
                    #db_type = st.radio("Select Database Type", ("MSSQL","MySQL"))
                    #st.write("Select Database Type")
                    db_type = st.selectbox("Select Database Type", options=["MSSQL", "MySQL"],help='Make sure DB should be public and allow relevant port in inbound rule')
                    
                    if db_type=="MSSQL":
                        # Input fields with placeholder text
                        host = st.text_input("Host", placeholder="your-rds-endpoint")
                        database = st.text_input("Database", placeholder="your_database")
                        user = st.text_input("Username", placeholder="your_username")
                        password = st.text_input("Password", type="password", placeholder="your_password")

                        if st.button("Connect to MSSQL"):
                            if not host or not database or not user or not password:
                                st.error("Please fill in all the fields before connecting!")
                            with st.spinner("Connecting to MSSQL database..."):
                                db = dc.rds_mssql_database(host, database, user, password)
                                if isinstance(db, str):
                                    # If the result is a string, it means an error occurred (connection failed)
                                    st.warning(db)
                                else:
                                    st.session_state.db = db
                                    st.success("Connected to MSSQL database!")
                    elif db_type=="MySQL":
                        st.warning("MySQL support is currently unavailable. Please select MSSQL instead.")
                elif creds=="No":
                    st.markdown('<p class="success-message">Don\'t worry.<br> You can use my credentials by hitting "Connect to Test DataBase"</p>', unsafe_allow_html=True)

                    # st.text_input("Host", value="ASHRITH\\sqlexpress", key="Host",type="password")
                    # st.text_input("Database", value="SQL_Learning", key="Database",type="password")
                    st.session_state['Host']="ASHRITH\\sqlexpress"
                    st.session_state['Database']="project_db"
                    if st.button("🌀 Connect to Test DataBase"):
                        with st.spinner("Connecting to MSSQL database..."):
                            db = dc.test_mssql_database(
                                st.session_state["Host"],
                                st.session_state["Database"]
                            )
                            st.toast('Connected!Now test me', icon='😍')
                            st.session_state.db = db
                            st.session_state.is_connected = True
                            st.success("Connected to MSSQL database!")
            if st.session_state.get('is_connected', False): 
                with st.expander("Table Details"):
                    show_table.display_table()
            
    elif selected == "Excel":
        with st.sidebar:
            st.session_state.excel = excel_page.get_excel()
            # Show button only if Excel data is loaded successfully
            if st.session_state.excel:
                st.session_state['Host'] = "ASHRITH\\sqlexpress"
                st.session_state['Database'] = "excel_data_storage"
                
                with st.spinner("Connecting to MSSQL database..."):
                    db = dc.test_mssql_database(
                        st.session_state["Host"],
                        st.session_state["Database"]
                    )
                    st.session_state.db = db
                    #st.session_state.is_connected = True  # Update connection flag
                    st.session_state.connect_clicked = False  # Reset button click flag
                    st.toast('Connected! Now test me', icon='😍')

            # # Show connection status to the user
            # if st.session_state.is_connected:
            #     st.sidebar.success("Connected to the database successfully!")
# Optional: Display connection status in the sidebar
# if st.session_state.is_connected:
#     st.sidebar.success("Connected to the database successfully!")
    
            # if st.session_state.get('is_connected', False): 
            #     with st.expander("Table Details"):
            #         show_table.display_table()
        
        
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)

    user_query = st.chat_input("Type a message...")
    if user_query is not None and user_query.strip() != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
            st.markdown(response)

        st.session_state.chat_history.append(AIMessage(content=response))


# page_bg_img = '''
    # <style>
    # body {
    # background-image: url("https://pngimg.com/uploads/linkedIn/linkedIn_PNG8.png");
    # background-size: cover;
    # }
    # </style>
    # '''

    # st.markdown(page_bg_img, unsafe_allow_html=True)
    
    
        #     linkedin_url = "https://www.linkedin.com/in/ladi-asrith-3aa49b248/"  # Replace with your LinkedIn profile URL
    #     linkedin_icon = (
    #     '<a href="' + linkedin_url + '" target="_blank">'
    #     '<img src="https://pngimg.com/uploads/linkedIn/linkedIn_PNG8.png" '
    #     'alt="LinkedIn" width="30" height="30" style="margin-top: 0px; margin-bottom: 0px;"/>'
    #     '</a>'
    # )
        

    # # Display LinkedIn icon at the top of the Streamlit page
        #st.markdown(linkedin_icon, unsafe_allow_html=True)