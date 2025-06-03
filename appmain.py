import streamlit as st
import pickle
import gzip
import requests
import os
import pandas as pd

# Google Drive direct download link
SIMILARITY_URL = "https://drive.google.com/uc?id=1byT7LzoLCZYErBBZNk0WqPo0AM1qsc2f"
SIMILARITY_FILE = "similarity.pkl.gz"

# Download similarity.pkl.gz if it doesn't exist
if not os.path.exists(SIMILARITY_FILE):
    st.info("Downloading similarity matrix...")
    response = requests.get(SIMILARITY_URL)
    with open(SIMILARITY_FILE, 'wb') as f:
        f.write(response.content)
    st.success("Download complete.")

# Load compressed similarity matrix
with gzip.open(SIMILARITY_FILE, 'rb') as f:
    similarity = pickle.load(f)

# Load movie dictionary
with open("movie_dict.pkl", "rb") as f:
    movies = pickle.load(f)

# Convert to DataFrame if needed
if isinstance(movies, dict):
    movies = pd.DataFrame(movies)

# Function to fetch poster using OMDb API
def fetch_poster(movie_title):
    api_key = "8e683932"
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    poster_url = data.get('Poster')
    return poster_url if poster_url and poster_url != 'N/A' else "https://via.placeholder.com/500x750?text=No+Poster"

# Recommend function
def recommend(movie):
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

# UI
st.header("🎬 Movie Recommender System")

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Type or select a movie", movie_list)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)
    if names and posters:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
