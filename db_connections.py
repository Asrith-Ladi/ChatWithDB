from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from langchain_community.utilities import SQLDatabase


def rds_mssql_database(host: str, database: str, user: str, password: str) -> SQLDatabase:
    try :
        db_uri = f"mssql+pyodbc://{user}:{password}@{host}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
        #engine = create_engine(db_uri)
        db=SQLDatabase.from_uri(db_uri)
        return db
    except Exception as e:
    # Catch other types of exceptions (network errors, timeout errors, etc.)
        # Provide feedback for connection errors related to credentials or network issues
        if "A network-related or instance-specific error" in str(e):
            return "Login failed 😟😟😟. Let me help you 🤝  1)Please check your host, database,username or password.2)Make sure SQL Server is configured to allow remote connections especially ports"
        else:
            # General Operational Error message
            return "Connection failed. Please check the host, database, username, and password. Error Details : {str(e)}"


def mssql_connection(host, database, user, password):
    #print(host, database, user, password)
    engine = create_engine(f"mssql+pyodbc://{user}:{password}@{host}/{database}?driver=ODBC+Driver+17+for+SQL+Server")
    
    return engine

        
# Function for initializing MSSQL connection
# def test_mssql_database(host: str, database: str) -> SQLDatabase:
#     db_uri = f"mssql+pyodbc://{host}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
#     db=SQLDatabase.from_uri(db_uri)
#     return db