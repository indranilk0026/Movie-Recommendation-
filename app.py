import random
import pickle
import requests
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#         poster_path = data.get('poster_path')
#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500/" + poster_path
#     except requests.exceptions.RequestException:
#         pass
#
#     return "https://via.placeholder.com/500x750?text=No+Poster+Available"


@st.cache_resource
def load_similarity():
    with open("movies_new.pkl", "rb") as f:
        movies = pickle.load(f)

    cv = CountVectorizer(max_features=5000, stop_words="english")
    vectors = cv.fit_transform(movies["tags"]).toarray()
    similarity = cosine_similarity(vectors)

    return movies, similarity

movies, similarity = load_similarity()


def recommend(movie, top_n=5):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = sorted(enumerate(similarity[movie_index]), reverse=True, key=lambda item: item[1])
    recommendations = []

    for idx, score in distances[1 : top_n + 1]:
        movie_row = movies.iloc[idx]
        recommendations.append(
            {
                "title": movie_row["title"],
                "movie_id": int(movie_row["movie_id"]),
                "score": round(float(score), 3),
            }
        )

    return recommendations


st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="centered")

st.title("🎬 Smart Movie Recommender")
st.write("Pick a movie, search quickly, and discover similar favorites in a few clicks.")

st.caption("This app uses movie similarity to suggest films with a similar feel.")

movie_titles = sorted(movies["title"].dropna().astype(str).tolist())

with st.sidebar:
    st.header("Explore")
    st.write("Search by title or choose from the full list.")
    search_query = st.text_input("Search for a movie", placeholder="Try 'Inception' or 'Avatar'")
    st.write(f"Available movies: {len(movie_titles)}")

search_query = search_query.strip().lower() if "search_query" in locals() else ""
filtered_titles = [title for title in movie_titles if search_query in title.lower()] if search_query else movie_titles

if not filtered_titles:
    st.warning("No movies matched your search. Showing the full list instead.")
    filtered_titles = movie_titles

if "current_movie" not in st.session_state:
    st.session_state.current_movie = None

selected_movie = st.selectbox(
    "Choose a movie",
    filtered_titles,
    index=None,
    placeholder="Select a movie..."
)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🔎 Show recommendations"):
        if selected_movie == "Select a movie" or selected_movie is None:
            st.info("Please choose a movie first.")
        else:
            st.session_state.current_movie = selected_movie
            st.session_state.recommendations = recommend(selected_movie)
with col2:
    if st.button("🎲 Surprise me"):
        random_movie = random.choice(movie_titles)
        st.session_state.current_movie = random_movie
        st.session_state.recommendations = recommend(random_movie)
        st.success(f"Showing recommendations for {random_movie}")

if "recommendations" in st.session_state:
    movie_label = st.session_state.current_movie or "your selection"
    st.subheader(f"Similar movies to: {movie_label}")
    if st.session_state.recommendations:
        for index, rec in enumerate(st.session_state.recommendations):
            st.write(f"{index + 1}. {rec['title']}")
    else:
        st.info("No recommendations found for this selection.")
else:
    st.info("Press the button above to generate movie suggestions.")


