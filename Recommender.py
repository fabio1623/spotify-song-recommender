import streamlit as st
import pandas as pd
from millify import millify
import functions as fc

st.set_page_config(
    page_title="Spotify-recommender App",
    page_icon="🎧",
    layout="wide"
)

if 'selected_match' not in st.session_state:
    st.session_state['selected_match'] = None

st.title("🎧 Spotify Song Recommender")
st.markdown('##### This project is still under construction.')

data = fc.load_data()
artists = fc.get_unique_artists(data)

st.sidebar.subheader(f"Here, you can select an artist over the {millify(len(artists), precision=1)} available.")
artist_pattern = st.sidebar.text_input("🗣️ Artist name :")
filtered_artists = fc.filter_artists(artists, artist_pattern)
selected_artist = st.sidebar.selectbox(
        label=f"{millify(len(filtered_artists), precision=1)} artist(s). Select one :",
        options=filtered_artists)

st.sidebar.subheader(f"Here, you can filter out songs by title. There are currently {millify(data.shape[0], precision=1)} available.")
name_pattern = st.sidebar.text_input("🎧 Song title :")

matches_tab, recommendation_tab = st.tabs(["🔍 Match(es)", "🔮 Recommendation"])

with matches_tab:
    matches = pd.DataFrame()
    if (selected_artist is None or selected_artist.strip() == '') and (name_pattern.strip() == ''):
        st.success('👈 Use at least 1 filter from the sidebar.')
    else:
        matches = fc.search_matches(data, selected_artist, name_pattern)
        st.markdown(f'##### {matches.shape[0]} match(es) found.')
        fc.display_matches(matches)

selected_match = st.session_state['selected_match']
if selected_match is not None:
    fc.display_song_summary_sidebar(selected_match)

with recommendation_tab:
    selected_match = st.session_state['selected_match']
    if matches.shape[0] == 0 or selected_match is None:
        st.success('👆 Select a matching song from the "Match(es)" tab.')
    else:
            left_col, right_col = st.columns(2)

            recommendation = fc.get_recommended_song(data, selected_match['_id']).iloc[0]
            if st.button("♻️ Recommend something different"):
                recommendation = fc.get_recommended_song(data, selected_match['_id']).iloc[0]

            with left_col:
                st.subheader("Your song :")
                fc.display_song_summary_body(selected_match)

            with right_col:
                st.subheader("Recommended song :")
                fc.display_song_summary_body(recommendation)

            columns_to_display = [col for col in matches.columns if col not in ['_id', 'artists', 'name', 'cluster', 'audio_features.duration_ms', 'audio_features.tempo']]
            
            plot = fc.plot_scatter_polar(selected_match, recommendation,  columns_to_display)
            st.plotly_chart(plot, use_container_width=True)