import os
import streamlit as st
import uuid
import pyttsx3

# --------------------------
# Function: Convert text to speech
# --------------------------
def text_to_speech(text, voice_choice, folder="audio_files"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = f"output_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(folder, filename)

    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    # Default to first voice if nothing matches
    selected_voice = voices[0].id if voices else None

    # Try to pick based on Male/Female
    if voice_choice == "Male":
        for v in voices:
            if "david" in v.name.lower() or "male" in v.name.lower():
                selected_voice = v.id
                break
    elif voice_choice == "Female":
        for v in voices:
            if "zira" in v.name.lower() or "female" in v.name.lower():
                selected_voice = v.id
                break
        # fallback to second voice if available
        if selected_voice == voices[0].id and len(voices) > 1:
            selected_voice = voices[1].id

    engine.setProperty("voice", selected_voice)
    engine.save_to_file(text, filepath)
    engine.runAndWait()
    return filepath


# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(page_title="Text to Speech", page_icon="🎙️", layout="centered")
st.title("🎙️ Text to Speech App")

# Text input area
user_text = st.text_area("Enter text here:", placeholder="Type something...")

# Dropdown for voice selection (default is placeholder)
voice_choice = st.selectbox("Choose Voice:", ["-- Select Voice --", "Male", "Female"])

# Generate audio when text & valid voice selected
if user_text.strip() != "" and voice_choice in ["Male", "Female"]:
    filepath = text_to_speech(user_text, voice_choice)
    with open(filepath, "rb") as audio_file:
        st.audio(audio_file.read(), format="audio/mp3")

