import streamlit as st

# Custom CSS to apply Aptos font
aptos_css = """
<style>
    @font-face {
        font-family: 'Aptos';
        src: url('https://example.com/path-to-aptos-font.woff2') format('woff2'),
             url('https://example.com/path-to-aptos-font.woff') format('woff');
    }
    html, body, [class*="css"] {
        font-family: 'Aptos', sans-serif;
    }
</style>
"""

# Apply the CSS
st.markdown(aptos_css, unsafe_allow_html=True)

# Version History in descending order
version_history = [
    {"version": "3.0", "features": ["Whats new! added","Demo video added"]},
    {"version": "2.8", "features": ["Testing DB added","Demo option added"]},
    {"version": "2.6", "features": [
        "Latency reduced while querying",
        "Data existed in tables is displayed by choosing table name in connected DB"
    ]},
    {"version": "2.4", "features": [
        "Admin page added",
        "Storing conversation history"
    ]},
    {"version": "2.2", "features": [
        "Social media accounts redirection added",
        "Feedback option added"
    ]},
    {"version": "2.0", "features": [
        "Displaying preview of data (Excel)",
        "Loading to DB"
    ]},
    {"version": "1.8", "features": [
        "Supported to get data from user via Excel",
        "Choosing sheet functionality added"
    ]},
    {"version": "1.4", "features": [
        "Login page introduced",
        "Secured password storing",
        "Forgot credentials process added",
        "Animations added"
    ]},
    {"version": "1.3", "features": ["Supported to AWS RDS MSSQL"]},
    {"version": "1.0", "features": [
        "Supported to local MSSQL Express",
        "Replied to current questions"
    ]}
]

# Display in the sidebar
st.sidebar.title("What's New")
for version in version_history:
    st.sidebar.subheader(f"Version {version['version']}")
    for feature in version['features']:
        st.sidebar.markdown(f"- {feature}")
st.video("https://youtu.be/vgvVVw0ZKjk")