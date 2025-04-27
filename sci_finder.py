import streamlit as st
import polars as pl
import json


st.sidebar.markdown(
"Get your recommendations! Just type in a book to discover the most similar ones"
)

st.write('''
## Find similar books

The following tool shows the top 10 books that are most similar to the given one in terms of their descriptions, according to a BM-25 
based recommender system.  
Please note: trivial recommendations will be given!  
For a more personalized experience, go to the "Taste Calibration" page.
''')

## load a .json file as a dictionary
@st.cache_data
def get_json(filename):
    with open (filename, "r") as f:
        data = json.load(f)
    return data

# book dataframe
books = pl.read_csv("sf_books_tidy.csv")
# book dataframe with column "Book" = "title, author"
books = books.with_columns(
    pl.concat_str(["Book_Title", "Author_Name"], separator=", ").alias("Book")
)

# top 50 BM25 recommendations
BM25recs = get_json("BM25recs_extended.json")

given_book = st.selectbox(
    "Select a book",
    books.select("Book"),
    index=2
)

# top 50 recs for a single book
top50 = pl.DataFrame({
    "Most similar books": BM25recs[given_book]
    })
top10 = pl.DataFrame({
    "Top 10 most similar books": BM25recs[given_book][:10]
    })
html_top10 = top10.to_pandas().to_html(index=False, classes="custom-table")

# dataframe containing only the recommended books with less than 100k ratings
less_pop = books.join(top50, how = "semi", left_on = "Book", right_on = "Most similar books")
less_pop = less_pop.filter(pl.col("Rating_votes") < 100000).select(pl.col("Book").alias("Similar but less popular books"))
html_less_pop = less_pop.head(10).to_pandas().to_html(index=False, classes="custom-table")

# dataframe containing only the recommended books that are not by the same author as given_book
# author of given_book
author = given_book.split(", ")[1]
top_different_authors = top50.filter(~pl.col("Most similar books").str.contains(author)).select(pl.col("Most similar books").alias("Similar books by a different author"))
html_top_different_authors = top_different_authors.head(10).to_pandas().to_html(index=False, classes="custom-table")

# dataframe containing only the recommended books that are not by the same author as given_book that have less than 100k ratings
top_everything = less_pop.join(top_different_authors, left_on="Similar but less popular books", right_on="Similar books by a different author", how = "semi").select(pl.col("Similar but less popular books").alias("Similar but less popular books by a different author"))
html_top_everything = top_everything.head(10).to_pandas().to_html(index=False, classes="custom-table")

# checkboxes (one for popularity, one for the author)
pop_check = st.checkbox("I don't want to see the same old books! Show me some that are lesser known")
author_check = st.checkbox("I'm really familiar with this author's literature, show me something by someone else")
# baseline (popular and by everyone)
if not pop_check and not author_check:
    st.markdown(html_top10, unsafe_allow_html=True)
# unpopular but by everyone
if pop_check and not author_check:
    st.markdown(html_less_pop, unsafe_allow_html=True)
# popular but by other authors
if not pop_check and author_check:
    st.markdown(html_top_different_authors, unsafe_allow_html=True)
# unpopular and by other authors
if pop_check and author_check:
    st.markdown(html_top_everything, unsafe_allow_html=True)

