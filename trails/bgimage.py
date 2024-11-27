# import streamlit as st
# import base64

# # Function to load local image as base64
# def load_image(image_file):
#     with open(image_file, "rb") as file:
#         encoded_image = base64.b64encode(file.read()).decode()
#     return f"data:image/png;base64,{encoded_image}"

# def bg_image(image):
#     # Set the background image and transparency using CSS
#     st.markdown(f"""
#         <style>
#             .stApp {{
#                 background-image: url('{load_image(image)}'); /* Set local image as background */
#                 background-size: cover; /* Ensure the image covers the entire background */
#                 background-position: center; /* Center the image */
#                 background-repeat: no-repeat;
#                 position: relative;
#                 height: 100vh; /* Full height */
#             }}
#             /* Adding an overlay for transparency */
#             .stApp::before {{
#                 content: '';
#                 position: absolute;
#                 top: 0;
#                 left: 60;
#                 width: 100%;
#                 height: 100%;
#                 background: rgba(0, 0, 0, 0.5); /* Black with 50% opacity */
#                 z-index: -1; /* Ensure the overlay is behind the content */
#             }}
#         </style>
#     """, unsafe_allow_html=True)

# bg_image('loginbg1.jpg')


