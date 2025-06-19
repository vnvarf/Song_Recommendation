import re
from deep_translator import GoogleTranslator

def clean_text(text):
    """
    Membersihkan teks dari simbol, angka, dan kapitalisasi.
    """
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower().strip()
    return text

def translate_to_english(text):
    """
    Menerjemahkan teks dari bahasa Indonesia (atau lainnya) ke bahasa Inggris.
    """
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text  # fallback jika API error