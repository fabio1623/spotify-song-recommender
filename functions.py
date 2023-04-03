import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import humanize

@st.cache_data
def load_data():
    return pd.read_csv("data/clusterized_data.csv")

@st.cache_data
def get_unique_artists(data):
    data['flattened_artists'] = data['artists'].str.split(',')
    data = data.explode('flattened_artists')
    unique_artists = data['flattened_artists'].unique()
    return sorted(unique_artists)

@st.cache_data
def get_number_unique_cluster(data):
    return len(data['cluster'].unique())

@st.cache_data
def get_mean_duration_ms(data):
    duration_ms = data['audio_features.duration_ms'].mean()
    duration_sec = duration_ms / 1000
    return humanize.precisedelta(duration_sec, minimum_unit="seconds", format="%0.2f")

@st.cache_data
def get_average_song_per_artist(data):
    return round(data.groupby("artists")["name"].count().mean())

@st.cache_data
def plot_duration_by_cluster(df):
    st.markdown(f'##### Average song duration (ms) per cluster')
    avg_duration = df.groupby('cluster')['audio_features.duration_ms'].mean()
    st.bar_chart(avg_duration)

@st.cache_data
def plot_tracks_by_cluster(df):
    st.markdown(f'##### Number of song per cluster')
    track_counts = df['cluster'].value_counts()
    st.bar_chart(track_counts)

def filter_artists(artists, pattern):
    if pattern.strip() == '':
        return []
    filtered_artists = [artist for artist in artists if pattern.lower() in artist.lower()]
    if len(filtered_artists) > 1:
        filtered_artists = [''] + filtered_artists
    return filtered_artists

@st.cache_data
def search_matches(df, artist_val=None, name_val=None):
    indexed_df = df.set_index(['name', 'artists'])
    filtered_df = indexed_df.copy()
    if artist_val is not None and artist_val != '':
        filtered_df = filtered_df.loc[filtered_df.index.get_level_values('artists').str.contains(artist_val)]
    if name_val is not None and name_val != '':
        filtered_df = filtered_df.loc[filtered_df.index.get_level_values('name').str.contains(name_val)]
    return filtered_df.reset_index()

def display_matches(filtered_data):
    selected_match = st.session_state['selected_match']

    if filtered_data.shape[0] > 0:
        st.markdown(f'##### Now, select your song in order to get a recommendation. 👇')

    st.write("---")

    for index, row in filtered_data.iterrows():
        display_song_summary_body(row)

        if st.button(f"👍 {row['_id']}"):
            if selected_match is None or selected_match['_id'] != row['_id']:
                st.session_state['selected_match'] = row
            else:
                st.session_state['selected_match'] = None

        st.write("---")

def display_song_summary_sidebar(song):
    st.sidebar.write("---")
    st.sidebar.subheader("Your selection")

    st.sidebar.write(f"🎯 : {song['_id']}")
    st.sidebar.write(f"🎧 : [{song['name']}](https://open.spotify.com/track/{song['_id']})")
    st.sidebar.write(f"🗣️ : {song['artists']}")

def display_song_summary_body(song):
    st.write(f"🎯 : {song['_id']}")
    st.write(f"🎧 : [{song['name']}](https://open.spotify.com/track/{song['_id']})")
    st.write(f"🗣️ : {song['artists']}")

def get_recommended_song(data, index):
    indexed_df = data.set_index('_id')
    filtered_df = indexed_df.copy()
    selected_row = filtered_df.loc[index]

    same_cluster = data[data['cluster'] == selected_row['cluster']]
    return same_cluster[same_cluster.index != selected_row.name].sample()

def plot_scatter_polar(selected_match, recommendation, columns_to_display):
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=selected_match[columns_to_display],
        theta=columns_to_display,
        fill='toself',
        name="Your Song",
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatterpolar(
        r=recommendation[columns_to_display],
        theta=columns_to_display,
        fill='toself',
        name="Recommendation",
        line=dict(color='red')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            )
        ),
        showlegend=True
    )

    return fig