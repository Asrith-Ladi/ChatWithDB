import streamlit as st

# Function to inject custom CSS styles
def set_custom_css():
    custom_css = """
    <style>
        /* Custom Font Style for Success Message */
        .success-message {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            font-size: 24px;
            color: green;
            font-weight: bold;
        }

        /* Custom Font Style for Warning Message */
        .warning-message {
            font-family: 'Arial', sans-serif;
            font-size: 22px;
            color: orange;
            font-weight: bold;
        }

        /* Custom Font Style for Information Message */
        .info-message {
            font-family: 'Courier New', monospace;
            font-size: 20px;
            color: blue;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

google_form_url = "https://forms.gle/i42119tA4YZgdyi27"  # Replace with your Google Form link   
feedback_button=f'<a href="{google_form_url}" target="_blank"><button style="font-size: 18px;  font-weight: bold;  background-color: #919E8B; color: #FEF8EF;border: 2px solid black; padding: 8px 18px; cursor: pointer; text-align: center;border-radius: 5px;margin-left: 10px; margin-top: 20px; "> Click me to give Feedback</button></a>'

# # Set custom CSS styles for fonts
# set_custom_css()

banner ="""
    <script>
    // Modify the decoration on top to reuse as a banner

    // Locate elements
    var decoration = window.parent.document.querySelectorAll('[data-testid="stDecoration"]')[0];
    var sidebar = window.parent.document.querySelectorAll('[data-testid="stSidebar"]')[0];

    // Observe sidebar size to adjust decoration position
    function outputsize() {
        decoration.style.left = `${sidebar.offsetWidth}px`;
    }

    new ResizeObserver(outputsize).observe(sidebar);

    // Adjust sizes and styling for the banner
    outputsize();
    decoration.style.height = "4.0rem";  // Height of the decoration
    decoration.style.right = "45px";     // Right margin

    // Adjust the background color to sunset gradient and text for the banner
    decoration.style.background = "linear-gradient(to right, #EBD2B9, #EBD2B9)";  // Sunset gradient
    decoration.style.color = "black";  // Black text color
    decoration.style.textAlign = "center";  // Center align the text
    decoration.style.display = "flex";  // Use flexbox to center the content vertically
    decoration.style.justifyContent = "left";  // Center horizontally
    decoration.style.alignItems = "left";  // Center vertically
    decoration.style.fontSize = "15px";  // Adjust the font size
    decoration.style.fontFamily = "'Aptos', sans-serif";  // Set font to Aptos
    decoration.style.color = "#6E7074";  // Set text color to #6E7074 (gray)
    decoration.style.fontWeight = "bold"; 
     // Make text bold

    // Add the text content with a message and line breaks
    decoration.innerHTML = 
    "<div style='margin-top: 0.5cm'>Hi, Thanks for being here.</div><br>" + 
Currently, I am in the testing phase, please consider that and share your experience/issues with me (via the contact tab on the right side).</div>";

    // Set the decoration behind other elements (like the 'Deploy' button)
    decoration.style.position = "absolute";  // Position it absolutely
    decoration.style.zIndex = "-1";  // Set the z-index lower to ensure it stays behind the 'Deploy' button
    decoration.style.width = "100%";  // Make the decoration span the full width of the page

    // Adjust the vertical position of the decoration (move it down by 0.5cm ~ 18.9px)
    decoration.style.top = "2.75px";// Move the banner 0.5 cm down
    </script>        
    """


