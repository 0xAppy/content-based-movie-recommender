import streamlit as st
import pickle
import pandas as pd
import requests

# similiarity File Processing
import os
import gdown

# Download similarity.pkl if not present
if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/uc?id=1W0SCyC3aKr81c1b2rViNYt4TSATosJi6"
    gdown.download(url, "similarity.pkl", quiet=False)


# Function to fetch movie poster
import requests

# Load movie data
movies = pickle.load(open('movies.pkl', 'rb'))

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie dropdown list
movie_titles = movies['title'].values

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        print("Movie ID:", movie_id)
        print(data)

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

        return "https://via.placeholder.com/300x450?text=No+Poster"

    except Exception as e:
        print("Error:", e)
        return "https://via.placeholder.com/300x450?text=Error"


def recommend_movie(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]

    distance = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distance)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    for i in movies_list:
        title = movies.iloc[i[0]]['title']
        movie_id = movies.iloc[i[0]]['id']

        print(title, movie_id)

        recommend_movies.append(title)
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies, recommend_movies_posters


st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    "Select a movie",
    movie_titles,
    index=None,
    placeholder="Choose a movie..."
)

if st.button('Recommend'):

    if selected_movie_name:

        names, posters = recommend_movie(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)

        cols = [col1, col2, col3, col4, col5]

        for idx, col in enumerate(cols):
            with col:
                st.text(names[idx])
                st.image(posters[idx])

    else:
        st.warning("Please select a movie first.")