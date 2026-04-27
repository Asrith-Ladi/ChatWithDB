import pytest
import db_connections

def test_rds_mssql_database_success(mocker):
    # Mock SQLDatabase.from_uri to avoid actual DB connection
    mock_from_uri = mocker.patch("db_connections.SQLDatabase.from_uri")
    
    # Setup mock return value
    mock_db_instance = mocker.MagicMock()
    mock_from_uri.return_value = mock_db_instance
    
    # Call the function
    result = db_connections.rds_mssql_database("test_host", "test_db", "test_user", "test_pass")
    
    # Verify
    expected_uri = "mssql+pyodbc://test_user:test_pass@test_host/test_db?driver=ODBC+Driver+17+for+SQL+Server"
    mock_from_uri.assert_called_once_with(expected_uri)
    assert result == mock_db_instance

def test_rds_mssql_database_network_error(mocker):
    # Mock to simulate a network error
    mock_from_uri = mocker.patch("db_connections.SQLDatabase.from_uri")
    mock_from_uri.side_effect = Exception("A network-related or instance-specific error occurred")
    
    result = db_connections.rds_mssql_database("test_host", "test_db", "test_user", "test_pass")
    
    # Check that the user-friendly network error message is returned
    assert "Login failed" in result
    assert "Please check your host" in result

def test_rds_mssql_database_general_error(mocker):
    # Mock to simulate a general exception
    mock_from_uri = mocker.patch("db_connections.SQLDatabase.from_uri")
    mock_from_uri.side_effect = Exception("Some weird database error")
    
    result = db_connections.rds_mssql_database("test_host", "test_db", "test_user", "test_pass")
    
    # Check that the general error message is returned
    assert "Connection failed" in result

def test_mssql_connection(mocker):
    # Mock create_engine
    mock_create_engine = mocker.patch("db_connections.create_engine")
    mock_engine_instance = mocker.MagicMock()
    mock_create_engine.return_value = mock_engine_instance
    
    result = db_connections.mssql_connection("test_host", "test_db", "test_user", "test_pass")
    
    expected_uri = "mssql+pyodbc://test_user:test_pass@test_host/test_db?driver=ODBC+Driver+17+for+SQL+Server"
    mock_create_engine.assert_called_once_with(expected_uri)
    assert result == mock_engine_instance
