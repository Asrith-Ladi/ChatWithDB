import streamlit as st
linkedin_url = "https://www.linkedin.com/in/ladi-asrith-3aa49b248/"  # Replace with your LinkedIn profile URL
linkedin_icon = (
'<a href="' + linkedin_url + '" target="_blank">'
'<img src="https://pngimg.com/uploads/linkedIn/linkedIn_PNG8.png" '
'alt="LinkedIn" width="30" height="30" style="margin-top: 0px; margin-bottom: 0px;"/>'
'</a>'
)
    

# Display LinkedIn icon at the top of the Streamlit page
st.markdown(linkedin_icon, unsafe_allow_html=True)