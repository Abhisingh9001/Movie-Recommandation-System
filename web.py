import streamlit as st
import pickle
import pandas as pd
import requests
import time

def fetch_poster(movie_id, retries=3):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=6caa086895b18967f7c7bfacaa0f5c78&append_to_response=videos,images'
    for _ in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return "https://image.tmdb.org/t/p/original/" + data['poster_path']
        except requests.exceptions.RequestException:
            time.sleep(1)  # Wait before retrying
    # Return a placeholder if all retries fail
    return "https://via.placeholder.com/300x450?text=No+Image"

# Load the similarity file
similarity = pickle.load(open(r"C:\Users\91979\similarity.pkl", 'rb'))  

# Load movie dictionary
movies_dict = pickle.load(open(r'C:\Users\91979\movie.to_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Function to recommend movies based on the selected movie
def recommend(movie):
    if movie in movies['title'].values:  # Check if movie exists
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movie = []
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movie, recommended_movies_posters
    else:
        return [], []

# Title of the app
st.title("Movie Recommendation System")

# Dropdown (selectbox) to select a movie title
selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

# Recommendation button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    
    if names and posters:
        with col1:
            st.text(names[0])
            st.image(posters[0]) 

        with col2:
            st.text(names[1])
            st.image(posters[1]) 
        with col3:
            st.text(names[2])
            st.image(posters[2]) 
        with col4:
            st.text(names[3])
            st.image(posters[3]) 
        with col5:
            st.text(names[4])
            st.image(posters[4]) 
    else:
        st.write("No recommendations found for the selected movie.")
