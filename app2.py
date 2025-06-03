import pickle
import streamlit as st
import requests
import pandas as pd
from io import BytesIO

# ------------------ GitHub URL for similarity.pkl ------------------
SIMILARITY_URL = "https://github.com/Vidushi2601/CineSuggest-Movie-Recommender-System/releases/download/v1.0-large-data/similarity.pkl"

@st.cache_data(show_spinner="Loading similarity matrix...")
def load_similarity():
    response = requests.get(SIMILARITY_URL)
    response.raise_for_status()
    similarity = pickle.load(BytesIO(response.content))
    return similarity

# ------------------ Local load for movie_dict.pkl ------------------
movies = pickle.load(open('movie_dict.pkl', 'rb'))
if isinstance(movies, dict):
    movies = pd.DataFrame(movies)

# ------------------ Fetch Poster from OMDb API ------------------
def fetch_poster(movie_title):
    api_key = "8e683932"  # Replace with your OMDb API key if needed
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    poster_url = data.get('Poster')
    if poster_url and poster_url != 'N/A':
        return poster_url
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# ------------------ Recommend Movies ------------------
def recommend(movie, movies, similarity):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found in the dataset.")
        return [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title
        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(fetch_poster(movie_title))
    return recommended_movie_names, recommended_movie_posters

# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

# Load similarity from GitHub
similarity = load_similarity()

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Type or select a movie from the dropdown", movie_list)

# Show recommendations
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie, movies, similarity)
    if names and posters:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
