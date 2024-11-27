import streamlit as st
import pandas as pd

# Sample DataFrame to display
data = {
    'ID': [1, 2, 3],
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35]
}
df = pd.DataFrame(data)


# Initialize session state variable
if 'show_table' not in st.session_state:
    st.session_state.show_table = False


# Button to open the table (toggle state)
if st.button('Click to Show Table',key=1):
    st.session_state.show_table = not st.session_state.show_table


# Display the table based on session state
if st.session_state.show_table:
    st.write("Table Data:")
    st.dataframe(df)

else:
    st.write("Click the button above to view the table.")
