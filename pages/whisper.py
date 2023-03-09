import openai
import streamlit as st
import os

st.set_page_config(layout="wide")

st.title('Transcription Audio → Texte')

# path = r'C:\Users\PFA\OneDrive - Axess OnLine\Bureau\open_ai\test-courchevel.mp3'
url = 'Interview contenu Megève-20230301_090229-Enregistrement de la réunion.mp4'

audio_input = st.file_uploader(
    label="Importer un fichier audio", 
    help="Fichiers limités à 25MB avec les types suivants : mp3, mp4.", 
    accept_multiple_files=True, 
    type=['mp3', 'mp4']
)

if audio_input is not None and st.button('Transcrire'): 
    i = 1
    for audio_file in audio_input:
        st.info("Fichier audio n°%s : %s" % (i, audio_file.name))
        if audio_file.type == "audio/mpeg":
            with open("fichier.mp3", "wb") as f:
                f.write(audio_file.getbuffer())
                transcript = openai.Audio.transcribe("whisper-1", open('fichier.mp3', 'rb'))["text"]
                st.write(transcript)
                # delete the file
            os.remove("fichier.mp3")
        i += 1
    
    st.success("La transcription a été réalisée avec succès.")
