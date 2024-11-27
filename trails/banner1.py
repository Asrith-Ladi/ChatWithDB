import streamlit as st

# Sidebar content
st.sidebar.header("Sidebar Title")
st.sidebar.subheader("Subheading")
st.sidebar.write("Sidebar content goes here.")

# Main content
st.title("Main Content")
st.write("Welcome to my Streamlit app!")
st.write("This is the main content area.")

# JS code to modify the decoration on top (banner-like behavior)
st.components.v1.html(
    """
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
    decoration.style.fontWeight = "bold";  // Make text bold

    // Add the text content with a message and line breaks
    decoration.innerHTML = "Hi, Thanks for being here.<br>\tCurrently, I am in the testing phase, please consider that and share your experience/issues with me (via the contact tab on the right side).<br>I hate confidential data, don't share it with me.";

    // Set the decoration behind other elements (like the 'Deploy' button)
    decoration.style.position = "absolute";  // Position it absolutely
    decoration.style.zIndex = "-1";  // Set the z-index lower to ensure it stays behind the 'Deploy' button
    decoration.style.width = "100%";  // Make the decoration span the full width of the page

    // Adjust the vertical position of the decoration (move it down by 0.5cm ~ 18.9px)
    decoration.style.top = "2.75px";// Move the banner 0.5 cm down
    </script>        
    """, width=10, height=0)
