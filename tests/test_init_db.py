import pytest
import init_db

def test_init_databases_and_tables_success(mocker):
    # Mock pyodbc.connect
    mock_connect = mocker.patch("pyodbc.connect")
    
    # Mock connection and cursor
    mock_conn = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()
    
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock fetchone to simulate that databases/tables DO NOT exist (so they get created)
    mock_cursor.fetchone.return_value = None
    
    dbs_to_create = ["db1", "db2"]
    
    # Run function
    result = init_db.init_databases_and_tables("host", "user", "pass", dbs_to_create)
    
    # Verify success
    assert result is True
    
    # Verify connection was called for master DB
    expected_master_conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=host;DATABASE=master;UID=user;PWD=pass;"
    mock_connect.assert_any_call(expected_master_conn_str, autocommit=True)
    
    # Verify database creation commands were executed
    mock_cursor.execute.assert_any_call("CREATE DATABASE [db1]")
    mock_cursor.execute.assert_any_call("CREATE DATABASE [db2]")
    
    # Verify table creation commands were executed
    mock_cursor.execute.assert_any_call("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'department'")
    mock_cursor.execute.assert_any_call("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'employee'")
    
def test_init_databases_and_tables_exception(mocker):
    # Mock pyodbc.connect to throw an exception
    mock_connect = mocker.patch("pyodbc.connect")
    mock_connect.side_effect = Exception("Connection Failed")
    
    # Mock st.error to verify it's called
    mock_st_error = mocker.patch("streamlit.error")
    
    result = init_db.init_databases_and_tables("host", "user", "pass", ["db1"])
    
    # Verify failure
    assert result is False
    
    # Verify streamlit error was displayed
    mock_st_error.assert_called_once()
    assert "Failed to initialize databases" in mock_st_error.call_args[0][0]
