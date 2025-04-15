import os
import tempfile
import base64
import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException

# Supported languages
LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu"
}

# Inject custom CSS
st.markdown("""
    <style>
        body {
            background-color: #f7f9fc;
        }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0,0,0,0.05);
        }
        h1 {
            text-align: center;
            color: #3b3b3b;
        }
        .stTextArea textarea {
            font-size: 16px;
            padding: 10px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            font-size: 16px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .audio-container {
            margin-top: 20px;
            text-align: center;
        }
        audio {
            width: 100%;
            outline: none;
        }
        .footer {
            margin-top: 3rem;
            background-color: #e8f0fe;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            font-size: 16px;
            font-weight: 500;
            color: #1a1a1a;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# App UI
st.markdown("<h1>🌐 Language Translator</h1>", unsafe_allow_html=True)

text_input = st.text_area("✍️ Enter text to translate", height=150)

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

source_lang_name = st.selectbox("🗣️ From Language", list(LANGUAGES.values()), index=0)
target_lang_name = st.selectbox("🎯 To Language", list(LANGUAGES.values()), index=1)

source_lang = [code for code, name in LANGUAGES.items() if name == source_lang_name][0]
target_lang = [code for code, name in LANGUAGES.items() if name == target_lang_name][0]

# Translate Button
if st.button("🔁 Translate"):
    if text_input:
        try:
            translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text_input)
            st.session_state.translated_text = translated
        except Exception as e:
            st.error(f"Translation error: {e}")

# Output Translated Text
if st.session_state.translated_text:
    st.text_area("✅ Translated Text", value=st.session_state.translated_text, height=150)

    # Play Audio
    if st.button("🔊 Listen to Translation"):
        try:
            tts = gTTS(text=st.session_state.translated_text, lang=target_lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                audio_path = fp.name

            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            audio_html = f"""
                <div class="audio-container">
                    <audio controls>
                        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                        Your browser does not support the audio tag.
                    </audio>
                </div>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
            os.remove(audio_path)

        except Exception as e:
            st.error(f"Audio error: {e}")

# Footer message
st.markdown("""
    <div class="footer">
        🚀 Made by <strong>Vinayak</strong> – Gen AI Developer
    </div>
""", unsafe_allow_html=True)
