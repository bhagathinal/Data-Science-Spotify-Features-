import streamlit as st 
import pandas as pd 
import plotly.express as px 

df = pd.read_csv("C:/Users/HINAL/Internship/Spotify/SpotifyFeatures.csv")

# Sidebar: Genre selection and Top N customization
st.sidebar.title("Genre and Top N Customization")
selected_genre = st.sidebar.selectbox("Select a Genre", df['genre'].unique())
top_n = st.sidebar.slider("Select Top N", min_value=1, max_value=50, value=10)

# Filter data based on selected genre
filtered_data = df[df['genre'] == selected_genre]

# Sidebar: Track selection
st.sidebar.title("Track Selection")
selected_track = st.sidebar.selectbox("Select a Track", filtered_data['track_name'].unique())

# Filter data based on selected track
selected_track_data = filtered_data[filtered_data['track_name'] == selected_track]

# Main content: Display statistics and visualizations
st.title("Music Analysis Dashboard")

# Display statistics for the selected genre
st.header(f"Statistics for {selected_genre} Genre")
st.write(f"Total Tracks: {len(filtered_data)}")
st.write(f"Average Popularity: {filtered_data['popularity'].mean():.2f}")
st.write(f"Average Danceability: {filtered_data['danceability'].mean():.2f}")

# Bar chart: Distribution of popularity for the selected genre
st.header(f"Distribution of Popularity for {selected_genre} Genre")
fig_popularity = px.histogram(filtered_data, x='popularity', nbins=20, title=f'Popularity Distribution - {selected_genre}')
st.plotly_chart(fig_popularity)

# Table: Top N tracks based on popularity
st.header(f"Top {top_n} Tracks for {selected_genre} Genre")
top_tracks = filtered_data.nlargest(top_n, 'popularity')[['track_name', 'artist_name', 'popularity']]
st.table(top_tracks)

# Table: Top N artists based on popularity
st.header(f"Top {top_n} Artists for {selected_genre} Genre")
top_artists = filtered_data.groupby('artist_name')['popularity'].mean().nlargest(top_n).reset_index()
st.table(top_artists[['artist_name', 'popularity']])

# Radar chart for selected track
st.title("Audio Features Radar Chart")

# Radar chart
fig_radar = px.line_polar(
    selected_track_data,
    r=['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence'],
    theta=['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Speechiness', 'Valence'],
    line_close=True,
    title=f'Audio Features Radar Chart - {selected_track}',
)
st.plotly_chart(fig_radar)

# Display numerical values for selected track
st.header(f"Audio Features for {selected_track}")
st.write(f"Acousticness: {selected_track_data['acousticness'].values[0]:.2f}")
st.write(f"Danceability: {selected_track_data['danceability'].values[0]:.2f}")
st.write(f"Energy: {selected_track_data['energy'].values[0]:.2f}")
st.write(f"Instrumentalness: {selected_track_data['instrumentalness'].values[0]:.2f}")
st.write(f"Liveness: {selected_track_data['liveness'].values[0]:.2f}")
st.write(f"Speechiness: {selected_track_data['speechiness'].values[0]:.2f}")
st.write(f"Valence: {selected_track_data['valence'].values[0]:.2f}")

