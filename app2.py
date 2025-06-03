import pickle
import streamlit as st
import requests
import pandas as pd


# Function to fetch poster using OMDb API
def fetch_poster(movie_title):
    api_key = "8e683932"  # Your OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    # OMDb returns 'Poster' key for poster URL, or 'N/A' if not available
    poster_url = data.get('Poster')
    if poster_url and poster_url != 'N/A':
        return poster_url
    else:
        # Placeholder image if no poster found
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
    for i in distances[1:6]:  # top 5 recommendations excluding selected movie itself
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
