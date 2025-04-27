import streamlit as st
import polars as pl
import json
import random

with open ("sf_books.json", "r") as f:
    books = json.load(f)

book_df = pl.DataFrame({
    "Book": books.keys(),
    "Description": books.values()
})

def random_book():
    random_key = random.choice(list(books.keys()))
    st.write("#### Book:")
    st.write(random_key)
    st.write("#### Synopsis:")
    st.write(books[random_key])

st.sidebar.markdown(
"Click the button and see if you've found a hidden gem 💎"
)

col1, col2, col3 = st.columns([1.5, 2, 1])

with col2:
    st.write("")
    button =  st.button("Click Here")
        
if button:
    random_book()








    
