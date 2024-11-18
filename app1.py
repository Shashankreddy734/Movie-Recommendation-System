'''import pandas as pd
import requests
from time import sleep
import base64
import streamlit as st
import pickle

# Function to add a background image from a local file
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode()  # Encode the image properly
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local('moviess.png')  # Add background image

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=3d4f7802e44a0ed98d868cb160f9e4dc&language=en-US",
            timeout=10  # Increase the timeout to 10 seconds
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to fetch cast and crew information
def fetch_cast_and_crew(movie_id, retries=3, delay=5):
    for i in range(retries):
        try:
            response = requests.get(
                f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=3d4f7802e44a0ed98d868cb160f9e4dc&language=en-US",
                timeout=10  # Increase the timeout to 10 seconds
            )
            response.raise_for_status()
            data = response.json()

            cast = [member['name'] for member in data['cast'][:5]]
            crew = [member['name'] for member in data['crew'] if member['job'] in ['Director', 'Producer']]

            return cast, crew
        except requests.exceptions.RequestException as e:
            if i < retries - 1:  # Not the last attempt
                st.warning(f"Retry {i + 1}/{retries} failed. Retrying in {delay} seconds...")
                sleep(delay)
            else:  # Last attempt
                st.error(f"Error fetching cast and crew after {retries} attempts: {e}")
                return [], []

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    recommended_movies_cast_crew = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

        # Fetch cast and crew details with retry mechanism
        cast, crew = fetch_cast_and_crew(movie_id)
        recommended_movies_cast_crew.append((cast, crew))

    return recommended_movies, recommended_movies_poster, recommended_movies_cast_crew

# Load the movie data
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

# Load the similarity matrix
similarity = pickle.load(open("similarity.pkl", "rb"))

# Streamlit app title (with red color)
st.markdown("<h1 style='color:red;'>Movie Recommender System</h1>", unsafe_allow_html=True)

# Dropdown menu for movie selection
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters, cast_crew_details = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    for col, name, poster, (cast, crew) in zip(columns, names, posters, cast_crew_details):
        with col:
            st.markdown(f'<p style="color:white;">{name}</p>', unsafe_allow_html=True)
            st.image(poster)
            st.markdown(f'<p style="color:white;">Cast: ' + ", ".join(cast) + '</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:white;">Crew: ' + ", ".join(crew) + '</p>', unsafe_allow_html=True)'''



import streamlit as st
import pickle
import pandas as pd
import requests
from time import sleep
import base64

# Function to add a background image from a local file
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode()  # Encode the image properly
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local('moviess.png')  # Add background image

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=3d4f7802e44a0ed98d868cb160f9e4dc&language=en-US",
            timeout=10  # Increase the timeout to 10 seconds
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to fetch cast and crew information
def fetch_cast_and_crew(movie_id, retries=3, delay=5):
    for i in range(retries):
        try:
            response = requests.get(
                f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=3d4f7802e44a0ed98d868cb160f9e4dc&language=en-US",
                timeout=10  # Increase the timeout to 10 seconds
            )
            response.raise_for_status()
            data = response.json()

            cast = [member['name'] for member in data['cast'][:5]]
            crew = [member['name'] for member in data['crew'] if member['job'] in ['Director', 'Producer']]

            return cast, crew
        except requests.exceptions.RequestException as e:
            if i < retries - 1:  # Not the last attempt
                st.warning(f"Retry {i + 1}/{retries} failed. Retrying in {delay} seconds...")
                sleep(delay)
            else:  # Last attempt
                st.error(f"Error fetching cast and crew after {retries} attempts: {e}")
                return [], []

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    recommended_movies_cast_crew = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

        # Fetch cast and crew details with retry mechanism
        cast, crew = fetch_cast_and_crew(movie_id)
        recommended_movies_cast_crew.append((cast, crew))

    return recommended_movies, recommended_movies_poster, recommended_movies_cast_crew

# Load the movie data
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

# Load the similarity matrix
similarity = pickle.load(open("similarity.pkl", "rb"))

# Initialize session state to keep track of history
if 'history' not in st.session_state:
    st.session_state.history = []

# Ask for the user's name and greet them
name = st.text_input("Please enter your name:")

if name:
    st.markdown(f'<p style="color:white;font-size:24px;">Hello, {name}! Welcome to the Movie Recommender System!</p>', unsafe_allow_html=True)

# Streamlit app title (with red color)
st.markdown("<h1 style='color:red;'>Movie Recommender System</h1>", unsafe_allow_html=True)

# Dropdown menu for movie selection
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters, cast_crew_details = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    for col, name, poster, (cast, crew) in zip(columns, names, posters, cast_crew_details):
        with col:
            st.markdown(f'<p style="color:white;">{name}</p>', unsafe_allow_html=True)
            st.image(poster)
            st.markdown(f'<p style="color:white;">Cast: ' + ", ".join(cast) + '</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:white;">Crew: ' + ", ".join(crew) + '</p>', unsafe_allow_html=True)

    # Add the selected movie and recommendations to history
    st.session_state.history.append({
        'movie': selected_movie_name,
        'recommendations': names
    })

# Display history
if st.button("Show History"):
    if st.session_state.history:
        st.markdown("<h3 style='color:white;'>Recent Activities:</h3>", unsafe_allow_html=True)
        for entry in st.session_state.history[-5:][::-1]:  # Show last 5 activities
            st.markdown(f"<p style='color:white;'>Selected Movie: {entry['movie']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:white;'>Recommended Movies: {', '.join(entry['recommendations'])}</p>", unsafe_allow_html=True)
            st.markdown("<hr style='order-color:white;'>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:white;'>No history available.</p>", unsafe_allow_html=True)