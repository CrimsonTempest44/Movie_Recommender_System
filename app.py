import pickle
import requests
import streamlit as st
import pandas as pd


def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=1b2c55b8a5f9a0423b5a81df5631a126')
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Ensure the 'poster_path' key exists in the response
        if 'poster_path' in data:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return None  # Return None if the poster path is not available
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        poster = fetch_poster(movie_id)
        if poster:
            recommended_movies_posters.append(poster)
        else:
            recommended_movies_posters.append("Poster not available")
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx], use_column_width=True)
