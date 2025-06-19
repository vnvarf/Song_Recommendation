import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
# import pyttsx3

# Load dataset Spotify
spotify_df = pd.read_csv("data/spotify/spotify_songs.csv")

# Mapping emosi ke valence
emotion_to_valence = {
    "happy": (0.6, 1.0),
    "sad": (0.0, 0.3),
    "angry": (0.4, 0.6),
    "surprise": (0.5, 0.8),
    "fear": (0.2, 0.4),
    "neutral": (0.4, 0.6)
}

# Fungsi rekomendasi lagu
def recommend_songs(emotion, df):
    if emotion == 'sad':
        songs = df[df['valence'] < 0.4]
    elif emotion == 'happy' or emotion == 'joy':
        songs = df[df['valence'] > 0.6]
    elif emotion == 'angry':
        songs = df[df['energy'] > 0.7]
    else:
        songs = df.sample(5)

    # Pilih kolom yang diperlukan
    return songs[['song_title', 'artist', 'valence', 'tempo', 'energy', 'danceability']].dropna()

# Radar chart
def radar_chart(df):
    features = ['valence', 'energy', 'danceability']
    avg_vals = df[features].mean()

    angles = np.linspace(0, 2 * np.pi, len(features), endpoint=False).tolist()
    values = avg_vals.tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), features)
    ax.set_ylim(0, 1)
    st.pyplot(fig)

# Text-to-speech offline (pyttsx3)
# def speak_offline(songs_df):
#     if songs_df.empty:
#         st.warning("Tidak ada lagu untuk dibacakan.")
#         return

#     texts = ["Berikut rekomendasi lagu untuk Anda:"]
#     for i, row in songs_df.iterrows():
#         texts.append(f"{row['song_title']} oleh {row['artist']}.")

#     full_text = " ".join(texts)

#     engine = pyttsx3.init()
#     engine.setProperty('rate', 150)
#     engine.setProperty('volume', 1.0)
#     engine.say(full_text)
#     engine.runAndWait()
