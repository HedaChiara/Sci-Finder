import streamlit as st
import polars as pl
import json
import random

# Dataframes
@st.cache_data
def get_json(filename):
    with open (filename, "r") as f:
        data = json.load(f)
    return data
books = pl.read_csv("sf_books_tidy.csv")
books = books.with_columns(
    pl.concat_str(["Book_Title", "Author_Name"], separator=", ").alias("Book")
)
# books that have been rated by users
ratings = get_json("PositiveRatings.json")
rated_books = []
for user in ratings.keys():
    for book in ratings[user]:
        if book not in rated_books:
            rated_books.append(book)

# top 50 BM25 recommendations
top50 = get_json("BM25recs_extended.json")


# sidebar text
st.sidebar.markdown(
"Select all your favourite books to discover what people with your same preferences also like!"
)

# cover links (https://bendodson.com/projects/itunes-artwork-finder/)
book_covers = {"Never Let Me Go, Kazuo Ishiguro" : "https://is5-ssl.mzstatic.com/image/thumb/Publication211/v4/e3/7a/c3/e37ac3af-39f8-ae66-eea0-07aa36c5911c/9781400044832.d.jpg/100000x100000-999.jpg",
               "Dune, Frank Herbert" : "https://is5-ssl.mzstatic.com/image/thumb/Publication122/v4/32/01/3b/32013b57-7d57-61f6-e8be-2c07b4cdc10b/9780575104419.jpg/100000x100000-999.jpg",
               "Blindness, José Saramago": "https://is5-ssl.mzstatic.com/image/thumb/Publication116/v4/93/c7/0d/93c70d1e-e2a7-4809-015c-2a9dedcffcbd/9780547537597.jpg/100000x100000-999.jpg",
               "The Hobbit, or There and Back Again, J.R.R. Tolkien" : "https://is5-ssl.mzstatic.com/image/thumb/Publication122/v4/8a/d8/61/8ad861cd-9c83-512c-d13e-022e625ef4b6/9780547951973.jpg/100000x100000-999.jpg",
               "The Island of Doctor Moreau, H.G. Wells" : "https://is5-ssl.mzstatic.com/image/thumb/Publication112/v4/ce/42/2b/ce422be2-e52b-766d-df31-5871f59f2006/The_Island_of_Doctor_Moreau.png/100000x100000-999.jpg",
               "Slaughterhouse-Five, Kurt Vonnegut Jr." : "https://is5-ssl.mzstatic.com/image/thumb/Publication123/v4/9d/6e/0e/9d6e0e88-3380-d95c-5fa3-26b521663b77/9780440339069.jpg/100000x100000-999.jpg",
               "Cloud Atlas, David Mitchell" : "https://m.media-amazon.com/images/I/81PK7KMw4IL._SL1500_.jpg",
               "The Martian, Andy Weir": "https://is5-ssl.mzstatic.com/image/thumb/Publication123/v4/d8/cf/30/d8cf306b-5f82-3529-9716-22af0fb27bea/9781473582323.jpg/100000x100000-999.jpg",
               "The Handmaid's Tale, Margaret Atwood" : "https://is5-ssl.mzstatic.com/image/thumb/Publication116/v4/61/f2/a0/61f2a0cb-71f7-e7e3-04f2-bbe93c5a2477/9780547345666.jpg/100000x100000-999.jpg",
               "11/22/63, Stephen King" : "https://is5-ssl.mzstatic.com/image/thumb/Publication211/v4/af/21/e2/af21e20c-c98d-543d-2a4b-1929d4571a2b/9781451627305.jpg/100000x100000-999.jpg",
               "The Man in the High Castle, Philip K. Dick" : "https://is5-ssl.mzstatic.com/image/thumb/Publication221/v4/de/5b/0c/de5b0c6e-aeed-a5b3-1e84-783098ce0a15/9780547601205.jpg/100000x100000-999.jpg",
               "Starship Troopers, Robert A. Heinlein" : "https://is5-ssl.mzstatic.com/image/thumb/Publication115/v4/7b/fc/4a/7bfc4aca-6284-b881-1c99-8f7075d092c6/9781101500422.jpg/100000x100000-999.jpg"
               }

# What about cyberpunk and steampunk? Are there user ratings available? <---------------------------------------------

covers = pl.DataFrame({
    "Book" : book_covers.keys(),
    "Cover" : book_covers.values()
}).to_pandas()

# Page text
st.write("### Select the books you like")

# saving selected books
selected = []

# 4 covers per row
cols = st.columns(4)
for idx, row in covers.iterrows():
    col = cols[idx % 4]
    with col:
        st.image(row["Cover"], use_container_width=True)
        if st.checkbox(f"{row['Book']}", key=f"img_{idx}"):
            # saving selected book in likes
            selected.append(row["Book"])
    # after every fourth image, the next one goes in another row
    if (idx + 1) % 4 == 0 and (idx + 1) < len(covers):
        cols = st.columns(4)

# selection of more books
st.write('''
#### If you don't like any of these books or you'd like to add some more to better capture your taste, you can select up to 3 more titles.
''')

book1 = st.selectbox(
    "Book 1",
    books.select("Book"),
    index = None,
    label_visibility = "collapsed",
    placeholder = "Book 1"
)
if book1:
    selected.append(book1)
book2 = st.selectbox(
    "Book 2",
    books.select("Book"),
    index = None,
    label_visibility = "collapsed",
    placeholder = "Book 2"
)
if book2:
    selected.append(book2)
book3 = st.selectbox(
    "Book 3",
    books.select("Book"),
    index = None,
    label_visibility = "collapsed",
    placeholder = "Book 3"
)
if book3:
    selected.append(book3)


# Recommendations
#st.write('''
# ## Here are your recommendations:
#''')

# Dictionary of users that have liked at least one of the selected books { id : number of books they both liked }
similar_users = {}
for user in ratings.keys():
    count = 0
    for liked_book in selected:
        if liked_book in ratings[user]:
            count += 1
    if count > 0:
        similar_users[user] = count
# getting the most similar ones (users that share the most liked books)
max_count = 1
for similar_user in similar_users:
    if similar_users[similar_user] > max_count:
        max_count = similar_users[similar_user]
# now, max_count contains the max number of books the current user and the others liked
# { id : liked books } only for the users that share max_count of books (also max_count-1 if max_count is at least 4) <- trying not to overfit
most_similar = {}
for similar_user in similar_users:
    if max_count > 3:
        if similar_users[similar_user] >= max_count-1:
            most_similar[similar_user] = ratings[similar_user]
    else:
        if similar_users[similar_user] == max_count:
            most_similar[similar_user] = ratings[similar_user]

# if none of the selected books are not in the rated books set, use the BM25 RS (e.g. 3BodyProblem, OnASunbeam, TheBalladOfSongbirdsAndSnakes)
# list of books that have not been rated by users
not_rated = []
for book in selected:
    if book not in rated_books:
        not_rated.append(book)
# { not_rated_book : [BM25_recs] }
not_rated_recs = {}
if not_rated == selected:
    tops = []
    # not recommending selected books
    for i in range(len(selected)):
        current_book = selected[i]
        other_books = selected.pop(i)
        selected.insert(i, current_book)
        # checking if books in selected appear in other selected books' recs
        for other in other_books:
            # eliminating those books from recs
            if other in top50[current_book]:
                top50[current_book].remove(other)
    if book1 and not book2 and not book3:
        tops = top50[book1][:10]
    if not book1 and book2 and not book3:
        tops = top50[book2][:10]
    if not book1 and not book2 and book3:
        tops = top50[book3][:10]
    elif book1 and book2 and not book3:
        top1 = top50[book1][:5]
        top2 = top50[book2][:5]
        tops = top1 + top2
    elif not book1 and book2 and book3:
        top2 = top50[book2][:5]
        top3 = top50[book3][:5]
        tops = top2 + top3
    elif book1 and not book2 and book3:
        top1 = top50[book1][:5]
        top3 = top50[book3][:5]
        tops = top1 + top3
    elif book1 and book2 and book3:
        top1 = top50[book1][:4]
        top2 = top50[book2][:3]
        top3 = top50[book3][:3]
        tops = top1 + top2 + top3
    if tops != []:
        tops_df = pl.DataFrame({"Recommendations" : tops})
        html_tops = tops_df.to_pandas().to_html(index=False, classes="custom-table")
        st.markdown(html_tops, unsafe_allow_html=True)
        

# for the recommendations, if at least one book is in the rated books set, I'm ignoring the ones that are not :)
rated = []
for book in selected:
    if book in rated_books:
        rated.append(book)

def get_recs():
    recs = []
    # list of books the most similar users liked
    for user in most_similar:
        for book in most_similar[user]:
            if book not in recs and book not in selected:
                recs.append(book)
    return recs

# returning a sample of the books the most similar users liked
if rated != []:
    tops = get_recs()
    if len(tops) >= 10:
        tops_df = pl.DataFrame({"Recommendations" : random.sample(tops, 10)})
    else:
        tops_df = pl.DataFrame({"Recommendations" : random.sample(tops, len(tops))})
    html_tops = tops_df.to_pandas().to_html(index=False, classes="custom-table")
    st.markdown(html_tops, unsafe_allow_html=True)

# centered "more recs" button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.write("")
    more = st.button("Get me some more recommendations", icon = "🔄")
        
if more:
    tops = get_recs()













