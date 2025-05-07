import streamlit as st
import polars as pl


st.markdown("""
<style>
/* Font sci-fi */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');
 

/* General Background */
.stApp {
    background-color: #0e1117;
    color: #ffffff;
    font-family: 'Orbitron', sans-serif;
}

/* Titles */
h1, h2, h3 {
    color: #00ffe7;
    font-weight: 600;
    text-shadow: 0 0 5px rgba(0,255,231,0.3);
}

/* Text */
p, div, label {
    color: #e0e0e0;
}

/* Buttons */            
div.stButton > button {
    background-color: #141821;
    color: #00ffe7;
    padding: 12px 28px;
    font-size: 16px;
    font-family: 'Orbitron', sans-serif;
    border-radius: 12px;
    border: 1px solid #00ffe7;
    transition: all 0.3s ease;
    box-shadow: none;
}

/* Hover */
div.stButton > button:hover {
    background-color: #1f2533;
    color: #00ffe7;
    box-shadow: 0 0 8px rgba(0, 255, 231, 0.3);
    transform: scale(1.02);
}

div.stButton > button:focus,
div.stButton > button:focus-visible,
div.stButton > button:focus-within {
    outline: none !important;
    box-shadow: none !important;
    border: 1px solid #00ffe7 !important;
    background-color: #1f2533 !important;
}

div.stButton > button::-moz-focus-inner {
    border: 0;
}

/* Input box */
input, textarea {
    background-color: #1a1f2b;
    color: #ffffff;
    border: 1px solid #00ffe7;
    border-radius: 8px;
    padding: 10px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #141821;
    color: #ffffff;
    padding: 20px;
    border-right: 1px solid #00ffe7;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    font-family: 'Orbitron', sans-serif !important;
    color: #e0e0e0 !important;
}
            
[data-testid="stSidebar"] .css-1cpxqw2,
[data-testid="stSidebar"] .css-qrbaxs,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #00ffe7 !important;
    font-family: 'Orbitron', sans-serif;
}

/* Sidebar Widgets */
[data-testid="stSidebar"] input {
    background-color: #1f2533;
    color: #ffffff;
    border: 1px solid #00ffe7;
    border-radius: 6px;
}
            
/* DataFrames */
div[data-testid="stDataFrame"] {
    background-color: #1f2533;
    border-radius: 8px;
    padding: 20px;
}

/* Table Style */
div[data-testid="stDataFrame"] table {
    font-family: 'Orbitron', sans-serif !important;
    color: #00ffe7 !important;
    width: 100%;
    border-collapse: collapse;
}

/* Cell Style */
div[data-testid="stDataFrame"] table td, div[data-testid="stDataFrame"] table th {
    border: 1px solid #00ffe7;
    padding: 8px;
    text-align: center;
}

/* Column Titles */
div[data-testid="stDataFrame"] table th {
    background-color: #141821;
    color: #00ffe7;
    font-weight: bold;
}

/* Alternate rows */
div[data-testid="stDataFrame"] table tr:nth-child(even) {
    background-color: #2b2e3b;
}

div[data-testid="stDataFrame"] table tr:nth-child(odd) {
    background-color: #1f2533;
}

/* Table Hover */
div[data-testid="stDataFrame"] table tr:hover {
    background-color: #00ffe7;
    color: #0e1117;
}

/* SelectBox */
div.stSelectbox > div > div > div {
    background-color: #1f2533;
    color: #00ffe7;
    border: 1px solid #00ffe7;
    border-radius: 8px;
    padding: 8px;
    font-family: 'Orbitron', sans-serif;
    font-size: 16px;
}
            
/* SelectBox Color */
div.stSelectbox div[role="listbox"] div[aria-selected="false"] {
    color: #2b2e3b !important;  /* Suggestions Color */
}
div.stSelectbox div[role="listbox"] div[aria-selected="true"] {
    color: #00ffe7 !important; 
}
div.stSelectbox > div > div > div input {
    color: #ffffff !important;  /* Written Text Color */
    background-color: #1f2533 !important; 
}

/* Hover and Focus*/
div.stSelectbox > div > div > div:focus {
    background-color: #2b2e3b;
    border-color: #00ffe7;
    color: #ffffff;
}

/* Selectbox */
div.stSelectbox select {
    background-color: #1f2533;
    color: #00ffe7;
    font-family: 'Orbitron', sans-serif;
    font-size: 16px;
    border: 1px solid #00ffe7;
    border-radius: 8px;
    padding: 8px;
    text-align: center;
}

/* Hover on Selectbox */
div.stSelectbox select:hover {
    background-color: #2b2e3b;
    border-color: #00ffe7;
}                    

.custom-table {
    margin-left: auto;
    margin-right: auto;
    width: 80%;
    border-collapse: collapse;
    font-family: 'Orbitron', sans-serif;
    background-color: #1f2533;
    border: 1px solid #00ffe7;
    border-radius: 10px;
    overflow: hidden;
}

.custom-table th {
    background-color: #141821;
    color: #e6f1ff;
    padding: 12px;
    text-align: center;
    border-bottom: 1px solid #00ffe7;
}

.custom-table td {
    color: #e6f1ff;
    padding: 10px;
    text-align: center;
    border-bottom: 1px solid #2b2e3b;
}

.custom-table tr:nth-child(even) {
    background-color: #2b2e3b;
}

div[data-testid="stDataFrame"] table tr:hover {
    background-color: #2b2e3b; 
    color: #e6f1ff; 
}
</style>
""", unsafe_allow_html=True)

# Define the pages
main_page = st.Page("sci_finder.py", title="Sci-Finder", icon="🚀")
personalize = st.Page("taste_calibration.py", title="Taste Calibration", icon="🧂")
rand = st.Page("random_recs.py", title="Feeling Lucky?", icon="🍀")

# Set up navigation
pg = st.navigation([main_page, personalize, rand]) # append other pages

# Run the selected page
pg.run()

# credits
st.sidebar.markdown(
    """
    <div style='position: fixed; bottom: 20px;'>
        <p style='margin-bottom: 5px;'><strong>Created by:</strong><br>
        Chiara Valentini<br>
        <p style='margin-top: 5px;'>
            <a href="https://github.com/HedaChiara" target="_blank" style="display: inline-block;">
                <img src="https://cdn.pixabay.com/photo/2022/01/30/13/33/github-6980894_1280.png" alt="GitHub" width="24" height="24">
            </a>
            <a href="https://www.linkedin.com/in/chiaravalentinistat/" target="_blank">
                <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" alt="LinkedIn" width="24" height="24">
            </a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

