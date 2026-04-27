import streamlit as st
import boto3
from botocore.exceptions import ClientError

def get_aws_keys():
    access_key = st.secrets.get("AWS_ACCESS_KEY_ID") or st.secrets.get("MSSQL", {}).get("AWS_ACCESS_KEY_ID")
    secret_key = st.secrets.get("AWS_SECRET_ACCESS_KEY") or st.secrets.get("MSSQL", {}).get("AWS_SECRET_ACCESS_KEY")
    return access_key, secret_key

def get_rds_client():
    access_key, secret_key = get_aws_keys()
    return boto3.client(
        'rds',
        region_name='ap-south-1',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

def is_db_available():
    try:
        client = get_rds_client()
        response = client.describe_db_instances(DBInstanceIdentifier="chatwithdb")
        instances = response.get('DBInstances', [])
        if instances:
            return instances[0].get('DBInstanceStatus') == 'available'
    except Exception:
        pass
    return False

def render_admin_panel():
    st.header("Admin Control Panel")
    
    if not st.session_state.get("admin_logged_in", False):
        st.info("Please login to access the admin panel.")
        admin_user = st.text_input("Admin Username")
        admin_pass = st.text_input("Admin Password", type="password")
        if st.button("Admin Login"):
            if admin_user == st.secrets["MSSQL"]["admin"] and admin_pass == st.secrets["MSSQL"]["admin_password"]:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        return

    if st.button("Admin Logout"):
        st.session_state.admin_logged_in = False
        st.rerun()
        
    st.subheader("AWS RDS Instance Management")
    
    access_key, secret_key = get_aws_keys()
    if not access_key or not secret_key:
        st.error("AWS credentials not found in secrets.toml.")
        return

    db_instance_id = "chatwithdb"
    
    try:
        client = get_rds_client()
        
        # Get DB status
        response = client.describe_db_instances(DBInstanceIdentifier=db_instance_id)
        instances = response.get('DBInstances', [])
        
        if not instances:
            st.error(f"Database instance '{db_instance_id}' not found.")
            return
            
        instance = instances[0]
        status = instance.get('DBInstanceStatus')
        
        st.write(f"**Database Name:** {db_instance_id}")
        
        # Display status with appropriate color
        if status == 'available':
            st.success(f"**Status:** {status.upper()}")
        elif status == 'stopped':
            st.error(f"**Status:** {status.upper()}")
        else:
            st.warning(f"**Status:** {status.upper()}")
            
        st.write("---")
        
        # Render Start/Stop buttons
        if status == 'stopped':
            if st.button("Start Database", type="primary"):
                with st.spinner("Starting database... This may take a few minutes."):
                    client.start_db_instance(DBInstanceIdentifier=db_instance_id)
                    st.success("Start command sent successfully! Please refresh to check status.")
                    st.rerun()
                    
        elif status == 'available':
            if st.button("Stop Database", type="primary"):
                with st.spinner("Stopping database... This may take a few minutes."):
                    client.stop_db_instance(DBInstanceIdentifier=db_instance_id)
                    st.success("Stop command sent successfully! Please refresh to check status.")
                    st.rerun()
            
            st.write("---")
            # Automatic Database Initialization
            if not st.session_state.get("db_auto_initialized", False):
                import init_db
                with st.spinner("Database is online! Verifying/initializing tables automatically..."):
                    host = st.secrets["MSSQL"]["host"]
                    user = st.secrets["MSSQL"]["user"]
                    password = st.secrets["MSSQL"]["password"]
                    dbs_to_create = [
                        st.secrets["MSSQL"]["database"],
                        st.secrets["MSSQL"]["db_excel"],
                        st.secrets["MSSQL"]["db_login"]
                    ]
                    if init_db.init_databases_and_tables(host, user, password, dbs_to_create):
                        st.session_state.db_auto_initialized = True
                        st.success("System verified: Databases and tables are ready for use!")
                    else:
                        st.error("Automatic initialization failed. Check your credentials.")
            
            st.write("---")
            st.write("### Registered Users")
            try:
                import pandas as pd
                import db_connections as dc
                host = st.secrets["MSSQL"]["host"]
                user = st.secrets["MSSQL"]["user"]
                password = st.secrets["MSSQL"]["password"]
                db_login = st.secrets["MSSQL"]["db_login"]
                
                engine = dc.mssql_connection(host, db_login, user, password)
                query = "SELECT id, username FROM Users"
                df = pd.read_sql(query, engine)
                st.dataframe(df, use_container_width=True, hide_index=True)
            except Exception as e:
                st.warning("Could not load users list. Please ensure the database is fully initialized.")
                    
        else:
            st.info("Database is currently transitioning. Please wait before attempting to start or stop.")
            if st.button("Refresh Status"):
                st.rerun()
                
    except ClientError as e:
        st.error(f"AWS Error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
