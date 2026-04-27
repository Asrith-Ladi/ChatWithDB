import pytest

@pytest.fixture(autouse=True)
def mock_streamlit_secrets(mocker):
    """
    Mock Streamlit's st.secrets globally for all tests, 
    so we don't need a real secrets.toml file during testing.
    """
    mock_secrets = {
        "MSSQL": {
            "host": "test_host",
            "database": "test_db",
            "user": "test_user",
            "password": "test_password",
            "db_excel": "test_db_excel",
            "db_login": "test_db_login"
        },
        "GROQ": {
            "api_key": "test_groq_api_key"
        }
    }
    
    # Mock both direct dictionary access and attribute access
    mocker.patch("streamlit.secrets", mock_secrets)
    return mock_secrets
