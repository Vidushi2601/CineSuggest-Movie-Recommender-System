import pickle
import streamlit as st
import requests
import pandas as pd
import os
import urllib.request

# Download similarity.pkl if it doesn't exist
SIMILARITY_URL = "https://drive.google.com/uc?id=1R1D7woHWIVK1HB97iHzW_41YL7Xf1pls"
SIMILARITY_FILE = "similarity.pkl"

if not os.path.exists(SIMILARITY_FILE):
    st.info("Downloading similarity matrix...")
    urllib.request.urlretrieve(SIMILARITY_URL, SIMILARITY_FILE)
    st.success("Download complete.")

# Function to fetch poster using OMDb API
def fetch_poster(movie_title):
    api_key = "8e683932"  # Your OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    poster_url = data.get('Poster')
    if poster_url and poster_url != 'N/A':
        return poster_url
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# Function to recommend similar movies
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

# Streamlit App
st.header('🎬 Movie Recommender System')

# Load data
movies = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Convert movies dict to DataFrame if needed
if isinstance(movies, dict):
    movies = pd.DataFrame(movies)

# Dropdown to select movie
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Type or select a movie from the dropdown", movie_list)

# Show recommendations
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    if names and posters:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
