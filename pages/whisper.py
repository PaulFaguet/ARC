import openai
import streamlit as st
import os
import nltk
from moviepy.editor import *
from dotenv import load_dotenv

load_dotenv()

nltk.download('punkt')

st.set_page_config(layout="wide")

st.title('Transcription Audio → Texte')

# path_to_file = st.secrets["AUDIO_FILE_PATH_MP3"]
path_to_file = os.getenv("AUDIO_FILE_PATH_MP3")

audio_input = st.file_uploader(
    label="Importer un ou plusieurs fichiers mp3", 
    help="Fichiers limités à 25MB avec le type mp3.", 
    accept_multiple_files=True, 
    type=['mp3']
)

# st.success("Type du fichier : %s" % audio_input[0].type)
if audio_input is not None and st.button('Transcrire'): 
    i = 1
    
    for audio_file in audio_input:
        st.info("Fichier audio n°%s : %s" % (i, audio_file.name))
        # if audio_file.type == "video/mp4":
        #     mp4_file = VideoFileClip(audio_file)
        #     mp4_file.audio.write_audiofile(path_to_file)
        # if audio_file.type == "audio/mpeg":
        audio_file_path = path_to_file
        with open(audio_file_path, "wb") as f:
            f.write(audio_file.getbuffer())
            transcript = openai.Audio.transcribe("whisper-1", open(audio_file_path, 'rb'))["text"]
            st.write(transcript)
            # delete the file
        os.remove(audio_file_path)
        i += 1
    
    st.success("La transcription a été réalisée avec succès.")
