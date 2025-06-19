import streamlit as st
from gtts import gTTS
from io import BytesIO
import pyttsx3
import pandas as pd
import joblib
import json
import os
from utils.preprocessing import clean_text
from utils.emotion_detector import detect_emotion
from utils.music_recommender import recommend_songs
from deep_translator import GoogleTranslator
import plotly.graph_objects as go

# def generate_tts_audio(text):
#     try:
#         tts = gTTS(text=text, lang='id')  # Gunakan 'en' untuk bahasa Inggris
#         mp3_fp = BytesIO()
#         tts.write_to_fp(mp3_fp)
#         mp3_fp.seek(0)
#         return mp3_fp
#     except Exception as e:
#         st.error(f"Gagal menghasilkan audio: {e}")
#         return None

# Text-to-speech offline (pyttsx3)
def speak_offline(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Gagal menjalankan TTS offline: {e}")

# Load model & asset
model = joblib.load("models/emotion_classifier.pkl")
emoji_map = json.load(open("assets/emoji_map.json"))
songs_df = pd.read_csv("data/spotify/spotify_songs.csv")

# CSS aksesibilitas
st.markdown("""
    <style>
        @font-face {
            font-family: 'OpenDyslexic';
            src: url('https://cdn.jsdelivr.net/gh/antijingoist/open-dyslexic/web/OpenDyslexic-Regular.otf') format('opentype');
        }
        html, body, [class*="css"] {
            font-family: 'OpenDyslexic';
        }
        .stButton>button {
            font-size: 1.5em;
            padding: 1em;
            background-color: black;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Judul
st.title("🎵 Emotion-Based Music Recommender")
st.subheader("Tulis perasaanmu hari ini…")

# Input user
user_input = st.text_area("", placeholder="Contoh: Aku sedang sangat bahagia!")

if user_input:
    # Preprocess + Translate
    cleaned = clean_text(user_input)
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(cleaned)
    except:
        translated = cleaned

    # Deteksi emosi
    detected_emotion = detect_emotion(model, translated)
    emoji = emoji_map.get(detected_emotion, "")

    st.markdown(f"### Kami mendeteksi bahwa kamu sedang merasa: **{detected_emotion}** {emoji}")

    # if st.button("🔊 Dengarkan Emosi Anda"):
    #     speak(f"Kami mendeteksi bahwa Anda sedang merasa {detected_emotion}")

    # Rekomendasi lagu
    st.markdown("---")
    st.markdown("## 🎶 Rekomendasi Lagu untuk Kamu")

    recommended = recommend_songs(detected_emotion, songs_df)
    st.dataframe(recommended[['song_title', 'artist', 'valence', 'tempo']])

    ## Tombol baca rekomendasi lagu
    if st.button("🔊 Baca Rekomendasi Lagu"):
        if not recommended.empty:
            text = "Berikut rekomendasi lagu untuk Anda. " + ". ".join(
                [f"{row['song_title']} oleh {row['artist']}" for _, row in recommended.iterrows()]
            )
            speak_offline(text)
        else:
            st.warning("Tidak ada lagu untuk dibacakan.")

    # Radar Chart
    st.markdown("### 🎛️ Visualisasi Fitur Lagu")
    fig = go.Figure()
    for i, row in recommended.head(3).iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row['valence'], row['energy'], row['danceability']],
            theta=['Valence', 'Energy', 'Danceability'],
            fill='toself',
            name=row['song_title']
        ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
    st.plotly_chart(fig)

else:
    st.info("Masukkan teks terlebih dahulu untuk mendapatkan rekomendasi.")
