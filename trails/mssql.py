from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import streamlit as st

# Function for initializing MSSQL connection
def init_mssql_database(host: str, database: str) -> SQLDatabase:
    db_uri = f"mssql+pyodbc://{host}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    return SQLDatabase.from_uri(db_uri)

# Function for initializing MySQL connection
def init_mysql_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)

def get_sql_chain(db):
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.

    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    

    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks. Please remove any '\_' in the query before execution.

    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    Question: Name 10 artists
    SQL Query: SELECT Name FROM Artist LIMIT 10;

    Your turn:

    Question: {question}
    SQL Query:
    """

    prompt = ChatPromptTemplate.from_template(template)

    #llm = ChatGroq(model="mixtral-8x7b-32768", groq_api_key="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", temperature=0)
    llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key="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", temperature=0)

    def get_schema(_):
        return db.get_table_info()

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
    Based on the table schema below, question, SQL query, and SQL response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}

    SQL Query: <SQL>{query}</SQL>

    User question: {question}
    SQL Response: {response}
    """

    prompt = ChatPromptTemplate.from_template(template)

    #llm = ChatGroq(model="mixtral-8x7b-32768", groq_api_key="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", temperature=0)
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
st.set_page_config(page_title="Chat with Database", page_icon=":speech_balloon:")
st.title("Chat with Database")

# Sidebar setup
with st.sidebar:
    st.subheader("Settings")
    db_type = st.radio("Select Database Type", ("MSSQL", "MySQL"))

    # MSSQL configuration inputs
    if db_type == "MSSQL":
        st.text_input("Host", value="ASHRITH\\sqlexpress", key="Host")
        st.text_input("Database", value="SQL_Learning", key="Database")
        if st.button("Connect to MSSQL"):
            with st.spinner("Connecting to MSSQL database..."):
                db = init_mssql_database(
                    st.session_state["Host"],
                    st.session_state["Database"]
                )
                st.session_state.db = db
                st.success("Connected to MSSQL database!")

    # MySQL configuration inputs
    elif db_type == "MySQL":
        st.text_input("Host", value="localhost", key="Host")
        st.text_input("Port", value="3306", key="Port")
        st.text_input("User", value="root", key="User")
        st.text_input("Password", type="password", value="", key="Password")
        st.text_input("Database", value="Chat_With_SQL", key="Database")
        if st.button("Connect to MySQL"):
            with st.spinner("Connecting to MySQL database..."):
                db = init_mysql_database(
                    st.session_state["User"],
                    st.session_state["Password"],
                    st.session_state["Host"],
                    st.session_state["Port"],
                    st.session_state["Database"]
                )
                st.session_state.db = db
                st.success("Connected to MySQL database!")

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
 