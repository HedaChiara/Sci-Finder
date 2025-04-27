import streamlit as st
import polars as pl
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');

/* General Background */
.stApp {
    background-color: #f6f9fc;
    color: #1a1a1a;
    font-family: 'Orbitron', sans-serif;
}

/* Titles */
h1, h2, h3 {
    color: #1f4e79;
    font-weight: 600;
    text-shadow: 0 0 4px rgba(31, 78, 121, 0.15);
}

/* Text */
p, div, label {
    color: #333333;
}

/* Buttons */
div.stButton > button {
    background-color: #e8f0fe;
    color: #1f4e79;
    padding: 12px 28px;
    font-size: 16px;
    border-radius: 12px;
    border: 1px solid #1f4e79;
    transition: all 0.3s ease;
}

/* Hover effect */
div.stButton > button:hover {
    background-color: #d0e3ff;
    box-shadow: 0 0 8px rgba(31, 78, 121, 0.2);
    transform: scale(1.02);
}

/* Input box */
input, textarea {
    background-color: #ffffff;
    color: #1a1a1a;
    border: 1px solid #1f4e79;
    border-radius: 8px;
    padding: 10px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #eef3f8;
    color: #1a1a1a;
    padding: 20px;
    border-right: 1px solid #ccddee;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    font-family: 'Orbitron', sans-serif !important;
    color: #1f4e79 !important;
}

/* DataFrames */
div[data-testid="stDataFrame"] {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 20px;
}

/* Table Style */
div[data-testid="stDataFrame"] table {
    font-family: 'Orbitron', sans-serif !important;
    color: #1f4e79 !important;
    width: 100%;
    border-collapse: collapse;
}

/* Cell Style */
div[data-testid="stDataFrame"] table td, div[data-testid="stDataFrame"] table th {
    border: 1px solid #ccddee;
    padding: 8px;
    text-align: center;
}

/* Column Titles */
div[data-testid="stDataFrame"] table th {
    background-color: #dfefff;
    color: #1f4e79;
    font-weight: bold;
}

/* Alternate rows */
div[data-testid="stDataFrame"] table tr:nth-child(even) {
    background-color: #f3f8ff;
}

div[data-testid="stDataFrame"] table tr:nth-child(odd) {
    background-color: #ffffff;
}

/* Table Hover */
div[data-testid="stDataFrame"] table tr:hover {
    background-color: #cce4ff;
    color: #0f2f4f;
}

/* SelectBox */
div.stSelectbox > div > div > div {
    background-color: #ffffff;
    color: #1f4e79;
    border: 1px solid #1f4e79;
    border-radius: 8px;
    padding: 8px;
}

/* SelectBox Dropdown */
div.stSelectbox div[role="listbox"] div[aria-selected="false"] {
    color: #666666 !important;
}
div.stSelectbox div[role="listbox"] div[aria-selected="true"] {
    color: #1f4e79 !important;
}

/* Custom Table */
.custom-table {
    margin-left: auto;
    margin-right: auto;
    width: 80%;
    border-collapse: collapse;
    font-family: 'Orbitron', sans-serif;
    background-color: #ffffff;
    border: 1px solid #ccddee;
    border-radius: 10px;
    overflow: hidden;
}

.custom-table th {
    background-color: #e3f1ff;
    color: #1f4e79;
    padding: 12px;
    text-align: center;
    border-bottom: 1px solid #ccddee;
}

.custom-table td {
    color: #1a1a1a;
    padding: 10px;
    text-align: center;
    border-bottom: 1px solid #e6ecf5;
}

.custom-table tr:nth-child(even) {
    background-color: #f6faff;
}
</style>
""", unsafe_allow_html=True)



# Define the pages
main_page = st.Page("scifinder.py", title="Sci-Finder", icon="🚀")
personalize = st.Page("personalization.py", title="Taste Calibration", icon="🧂")
rand = st.Page("random.py", title="Feeling Lucky?", icon="🍀")

# Set up navigation
pg = st.navigation([main_page, personalize, rand]) # append other pages

# Run the selected page
pg.run()

