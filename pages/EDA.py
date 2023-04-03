import streamlit as st
from millify import millify
import functions as fc

st.set_page_config(
    page_title="Spotify-recommender App",
    page_icon="🎧",
    layout="wide"
)

st.session_state['selected_match'] = None

st.title("🎧 Spotify Song EDA")
st.markdown('##### This project is still under construction.')

data = fc.load_data()
artists = fc.get_unique_artists(data)
nb_clusters = fc.get_number_unique_cluster(data)
mean_duration = fc.get_mean_duration_ms(data)
avg_song_per_artist = fc.get_average_song_per_artist(data)

overview_tab, avg_duration_tab, nb_song_tab = st.tabs(["Overview", "Average duration/cluster", "Number of songs/cluster"])

with overview_tab:
    st.markdown(f'##### 🎧 {millify(data.shape[0], precision=1)} songs')
    st.markdown(f'##### 🗣️ {millify(len(artists), precision=1)} artists')
    st.markdown(f'##### 🎯 {nb_clusters} clusters')
    st.markdown(f'##### 🕰️ {mean_duration} for a song on average')
    st.markdown(f'##### 📊 {avg_song_per_artist} songs per artist on average')

with avg_duration_tab:
    fc.plot_duration_by_cluster(data)

with nb_song_tab:
    fc.plot_tracks_by_cluster(data)