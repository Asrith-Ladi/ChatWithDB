import streamlit as st

# Custom CSS to increase the sidebar scrollbar width
st.markdown(
    """
    <style>
    /* Targeting the scrollbar of the sidebar */
    .css-1d391kg::-webkit-scrollbar {
        width: 10px;  /* Adjust width of the scrollbar */
    }

    .css-1d391kg::-webkit-scrollbar-thumb {
        background-color: rgba(0, 0, 0, 0.3);  /* Color of the scrollbar thumb */
        border-radius: 10px;
        /* Optional: round the edges of the thumb */
    }

    .css-1d391kg::-webkit-scrollbar-track {
        background: #f1f1f1;  /* Background color of the scrollbar track */
        border-radius: 10px; 
        /* Optional: round the edges of the track */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Your Streamlit app content
st.title("Custom Sidebar Scrollbar Width Example")

st.sidebar.header("Sidebar Header")
st.sidebar.text("This is the sidebar content. Scroll down to see the effect.")

# Add some dummy content to the sidebar to make the scrollbar visible
for i in range(50):
    st.sidebar.text(f"Item {i+1}")

st.write("This is the main content area of the app.")
