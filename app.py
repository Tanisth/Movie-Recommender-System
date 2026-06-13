import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=11fc9eb0600f005d26cb8e0e05558f60&language=en-US',
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        # Guard: poster_path can be None even on a successful response
        poster_path = data.get('poster_path')
        if not poster_path:
            return None

        return "https://image.tmdb.org/t/p/original" + poster_path

    except Exception as e:
        print("Poster fetch error:", e)
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]


    recommended_movies = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch posters from API
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movie_posters

movie_list = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movie_list)
if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/uc?id=10c30iWO8x_9aeLGVefwH-dCzHu_iCDSu"
    gdown.download(url, "similarity.pkl", quiet=False)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "So What's the mood today?",
    movies['title'].values,
    placeholder="Select The movie you would like to watch...",
)

def show_movie(col, name, poster):
    with col:
        st.subheader(name)
        if poster:
            st.image(poster)
        else:
            st.caption("🎬 Poster unavailable")

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        show_movie(col, name, poster)