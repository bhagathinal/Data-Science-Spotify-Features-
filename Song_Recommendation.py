import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import streamlit as st

# Load your dataset (replace 'your_dataset.csv' with your actual dataset file)
df = pd.read_csv('SpotifyFeatures.csv')

# Select relevant features for content-based recommendation
features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']

# Fill missing values with 0 or other appropriate values
df[features] = df[features].fillna(0)

# Combine features into a single string for each song
df['features'] = df[features].astype(str).agg(' '.join, axis=1)

# Create TF-IDF matrix
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['features'])

# Build NearestNeighbors model
nn_model = NearestNeighbors(n_neighbors=6, metric='cosine', algorithm='brute')
nn_model.fit(tfidf_matrix)

# Streamlit App
st.title('Song Recommendation App')

# User input for song recommendation
song_index = st.selectbox('Select a song:', df['track_name'].values)

# Find the index of the selected song
selected_index = df[df['track_name'] == song_index].index[0]

# Get the nearest neighbors of the selected song
_, indices = nn_model.kneighbors(tfidf_matrix[selected_index])

st.subheader('Top 5 Recommended Songs:')

# Display top 5 recommended songs
for i in range(1, 6):
    index = indices[0][i]
    st.write(f"{i}. Song: {df['track_name'].iloc[index]}, Artist: {df['artist_name'].iloc[index]}")
